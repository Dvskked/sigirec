document.addEventListener("DOMContentLoaded", () => {

    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const startCameraButton = document.getElementById("start-camera");
    const takePhotoButton = document.getElementById("take-photo");
    const cameraPlaceholder = document.getElementById("camera-placeholder");
    const scanFrame = document.getElementById("scan-frame");
    const scanLine = document.getElementById("scan-line");
    const scanResult = document.getElementById("scan-result");
    const scanLoading = document.getElementById("scan-loading");
    const resultTitle = document.getElementById("result-title");
    const resultDescription = document.getElementById("result-description");
    const resultPoints = document.getElementById("result-points-value");
    const resultImage = document.getElementById("result-image");
    const recycleButton = document.getElementById("recycle-button");
    const currentPoints = document.getElementById("current-points");
    const aiStatusText = document.getElementById("ai-status-text");
    const aiStatus = document.getElementById("ai-status");
    const detectionDetails = document.getElementById("detection-details");
    const retryMessage = document.getElementById("retry-message");
    const cameraWrapper = document.querySelector(".camera-wrapper");
    const cameraControls = document.querySelector(".camera-controls");
    const scannerHelp = document.querySelector(".scanner-help");
    const scanPage = document.querySelector(".scan-page");

    const modalOverlay = document.getElementById("sigi-modal-overlay");
    const modalIcon = document.getElementById("sigi-modal-icon");
    const modalTitle = document.getElementById("sigi-modal-title");
    const modalText = document.getElementById("sigi-modal-text");
    const modalPoints = document.getElementById("sigi-modal-points");
    const modalPointsValue = document.getElementById("sigi-modal-points-value");
    const modalComprobante = document.getElementById("sigi-modal-comprobante");
    const modalCompNum = document.getElementById("sigi-modal-comp-num");
    const modalBtn = document.getElementById("sigi-modal-btn");

    let stream = null;
    let cameraActive = false;
    let resultadoAnalisis = null;
    let isProcessing = false;

    const dashboardUrl = scanPage
        ? scanPage.getAttribute("data-dashboard-url")
        : "/dashboard";

    const MAX_RETRIES = 2;
    const FETCH_TIMEOUT = 55000;


    function showElement(el) {
        if (el) el.style.display = "";
    }

    function hideElement(el) {
        if (el) el.style.display = "none";
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(function(t) { t.stop(); });
            stream = null;
        }
        cameraActive = false;
    }

    function resetUI() {
        hideElement(scanResult);
        hideElement(scanLoading);
        if (retryMessage) retryMessage.style.display = "none";
        if (detectionDetails) {
            detectionDetails.style.display = "none";
            detectionDetails.innerHTML = "";
        }
        if (recycleButton) {
            recycleButton.style.display = "none";
            recycleButton.disabled = false;
            recycleButton.innerHTML = "<span>\u267B RECICLAR</span>";
        }
    }

    function showModal(config) {
        if (!modalOverlay) return Promise.resolve();

        modalIcon.className = "sigi-modal-icon " + (config.type || "success");
        modalIcon.textContent = config.type === "error" ? "\u2715" : "\u267B";
        modalTitle.textContent = config.title || "";
        modalText.textContent = config.text || "";

        if (config.points !== undefined) {
            modalPoints.style.display = "";
            modalPointsValue.textContent = config.points;
        } else {
            modalPoints.style.display = "none";
        }

        if (config.comprobante) {
            modalComprobante.style.display = "";
            modalCompNum.textContent = config.comprobante;
        } else {
            modalComprobante.style.display = "none";
        }

        modalBtn.className = "sigi-modal-btn" + (config.type === "error" ? " error-btn" : "");
        modalBtn.textContent = config.buttonText || "ACEPTAR";
        modalOverlay.classList.add("visible");

        return new Promise(function(resolve) {
            function handler() {
                modalOverlay.classList.remove("visible");
                modalBtn.removeEventListener("click", handler);
                resolve();
            }
            modalBtn.addEventListener("click", handler);
        });
    }

    function buildDetectionHTML(detecciones) {
        if (!detecciones || detecciones.length === 0) return "";
        var html = "";
        var iconMap = { "botella": "\u267B", "tapa": "\u25C9", "etiqueta": "\u25A4" };
        detecciones.forEach(function(det) {
            var icon = iconMap[det.clase] || "\u25CF";
            var conf = (det.confianza * 100).toFixed(1);
            html += '<div class="detection-item"><span>' + icon + '</span><strong>' +
                det.clase.toUpperCase() + '</strong><span>' + conf + '%</span></div>';
        });
        return html;
    }

    function reenableCamera() {
        takePhotoButton.disabled = false;
        startCameraButton.disabled = true;
        startCameraButton.innerHTML =
            '<span class="button-icon">\u2713</span><span>C\u00e1mara activa</span>';
    }


    // =====================================================
    // ENVIAR A FLASK CON RETRY
    // =====================================================

    function enviarAnalisis(formData, attempt) {
        var ctrl = new AbortController();
        var tid = setTimeout(function() { ctrl.abort(); }, FETCH_TIMEOUT);

        return fetch("/api/escanear", {
            method: "POST",
            body: formData,
            credentials: "same-origin",
            signal: ctrl.signal
        }).then(function(resp) {
            clearTimeout(tid);
            var ct = resp.headers.get("content-type") || "";
            if (ct.indexOf("application/json") === -1) {
                throw new Error("html");
            }
            return resp.json().then(function(data) {
                if (!resp.ok) {
                    throw new Error(data.error || "Error procesando la imagen.");
                }
                return data;
            });
        }).catch(function(err) {
            clearTimeout(tid);

            var isRecoverable =
                err.name === "AbortError" ||
                err instanceof TypeError ||
                (err.message && err.message === "html");

            if (isRecoverable && attempt < MAX_RETRIES) {
                var waitSec = (attempt + 1) * 3;
                if (aiStatusText) {
                    aiStatusText.textContent =
                        "Reintentando (" + (attempt + 1) + "/" + MAX_RETRIES + ") en " + waitSec + "s...";
                }
                showElement(scanLoading);

                return new Promise(function(resolve) {
                    setTimeout(resolve, waitSec * 1000);
                }).then(function() {
                    return new Promise(function(resolve, reject) {
                        canvas.toBlob(function(newBlob) {
                            if (!newBlob) { reject(new Error("blob")); return; }
                            var fd = new FormData();
                            fd.append("imagen", newBlob, "reciclaje.jpg");
                            enviarAnalisis(fd, attempt + 1).then(resolve, reject);
                        }, "image/jpeg", 0.90);
                    });
                });
            }

            if (err.message === "html") {
                throw new Error(
                    "El servidor no respondi\u00f3 correctamente. " +
                    "Puede estar inici\u00e1ndose, espera unos segundos e intenta de nuevo."
                );
            }
            if (err.name === "AbortError") {
                throw new Error(
                    "El servidor est\u00e1 tardando demasiado. " +
                    "Render free tier puede tardar al despertar, intenta de nuevo."
                );
            }
            throw err;
        });
    }

    function mostrarResultado(data) {
        resultadoAnalisis = data;

        hideElement(scanLoading);

        if (data.imagen && resultImage) {
            resultImage.src = "data:image/jpeg;base64," + data.imagen;
        }

        if (data.success && data.botella_detectada) {
            stopCamera();
            hideElement(cameraWrapper);
            hideElement(cameraControls);
            hideElement(scannerHelp);

            resultTitle.textContent = data.titulo || "\u00a1Botella reconocida!";
            resultDescription.textContent = data.mensaje || "La botella fue reconocida correctamente.";
            resultPoints.textContent = data.puntos || 0;

            if (detectionDetails && data.detecciones) {
                var html = buildDetectionHTML(data.detecciones);
                if (html) {
                    detectionDetails.innerHTML = html;
                    showElement(detectionDetails);
                }
            }

            if (retryMessage) retryMessage.style.display = "none";
            if (recycleButton) showElement(recycleButton);
            showElement(scanResult);
            return;
        }

        resultTitle.textContent = data.titulo || "Botella no reconocida";
        resultDescription.textContent = data.mensaje || "No se detect\u00f3 una botella v\u00e1lida.";
        resultPoints.textContent = "0";

        if (recycleButton) recycleButton.style.display = "none";
        if (retryMessage) showElement(retryMessage);
        showElement(scanResult);
        reenableCamera();
    }

    function mostrarError(msg) {
        hideElement(scanLoading);

        resultTitle.textContent = "Error en el an\u00e1lisis";
        resultDescription.textContent = msg || "No se pudo conectar con el servidor.";
        resultPoints.textContent = "0";

        if (recycleButton) recycleButton.style.display = "none";
        if (retryMessage) showElement(retryMessage);
        showElement(scanResult);
        reenableCamera();
    }


    // =====================================================
    // ACTIVAR CÁMARA
    // =====================================================

    startCameraButton.addEventListener("click", async function() {

        if (cameraActive && stream) return;
        resetUI();

        try {
            startCameraButton.disabled = true;
            startCameraButton.innerHTML =
                '<span class="button-icon">\u25cc</span><span>Activando c\u00e1mara...</span>';

            stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
                audio: false
            });

            video.srcObject = stream;
            video.style.display = "block";
            hideElement(cameraPlaceholder);

            await new Promise(function(resolve) {
                if (video.readyState >= 2) resolve();
                else video.onloadedmetadata = function() { resolve(); };
            });

            try { await video.play(); } catch (e) { console.warn("Video play:", e); }

            cameraActive = true;
            takePhotoButton.disabled = false;

            startCameraButton.innerHTML =
                '<span class="button-icon">\u2713</span><span>C\u00e1mara activa</span>';

            if (aiStatusText) aiStatusText.textContent = "C\u00e1mara activa";
            if (aiStatus) aiStatus.classList.add("active");

            showElement(scanFrame);
            showElement(scanLine);

        } catch (error) {
            console.error("ERROR C\u00c1MARA:", error);

            cameraActive = false;
            stream = null;
            startCameraButton.disabled = false;
            startCameraButton.innerHTML =
                '<span class="button-icon">\u2301</span><span>Escanear botella</span>';

            var msg = "No fue posible activar la c\u00e1mara.";
            if (error.name === "NotAllowedError") {
                msg = "Permiso de c\u00e1mara denegado. Permite el acceso desde el navegador.";
            } else if (error.name === "NotFoundError") {
                msg = "No se encontr\u00f3 ninguna c\u00e1mara.";
            } else if (error.name === "NotReadableError") {
                msg = "La c\u00e1mara est\u00e1 siendo utilizada por otra aplicaci\u00f3n.";
            }

            await showModal({ type: "error", title: "Error de c\u00e1mara", text: msg, buttonText: "ENTENDIDO" });
        }
    });


    // =====================================================
    // TOMAR FOTO
    // =====================================================

    takePhotoButton.addEventListener("click", async function() {

        if (!stream || !cameraActive || video.readyState < 2) {
            await showModal({
                type: "error",
                title: "C\u00e1mara inactiva",
                text: "Primero debes activar la c\u00e1mara.",
                buttonText: "ENTENDIDO"
            });
            return;
        }

        if (isProcessing) return;

        var width = video.videoWidth;
        var height = video.videoHeight;

        if (width === 0 || height === 0) {
            await showModal({
                type: "error",
                title: "C\u00e1mara no lista",
                text: "La c\u00e1mara todav\u00eda no est\u00e1 lista. Espera un momento e int\u00e9ntalo.",
                buttonText: "ENTENDIDO"
            });
            return;
        }

        canvas.width = width;
        canvas.height = height;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, width, height);

        var fotoCapturada = canvas.toDataURL("image/jpeg", 0.90);
        if (resultImage) resultImage.src = fotoCapturada;

        resetUI();
        hideElement(scanResult);
        showElement(scanLoading);

        takePhotoButton.disabled = true;
        startCameraButton.disabled = true;
        isProcessing = true;

        canvas.toBlob(async function(blob) {
            isProcessing = false;

            if (!blob) {
                hideElement(scanLoading);
                takePhotoButton.disabled = false;
                startCameraButton.disabled = false;
                await showModal({
                    type: "error",
                    title: "Error",
                    text: "No fue posible capturar la imagen.",
                    buttonText: "ENTENDIDO"
                });
                return;
            }

            var formData = new FormData();
            formData.append("imagen", blob, "reciclaje.jpg");

            try {
                var data = await enviarAnalisis(formData, 0);
                console.log("RESPUESTA API:", data);
                mostrarResultado(data);
            } catch (error) {
                console.error("ERROR ANALIZANDO:", error);
                mostrarError(error.message);
            }
        }, "image/jpeg", 0.90);
    });


    // =====================================================
    // BOTÓN RECICLAR
    // =====================================================

    recycleButton.addEventListener("click", async function() {

        if (!resultadoAnalisis || !resultadoAnalisis.botella_detectada) return;
        if (isProcessing) return;

        isProcessing = true;
        recycleButton.disabled = true;
        recycleButton.innerHTML =
            '<span class="button-spinner"></span><span>Procesando...</span>';

        try {
            var response = await fetch("/api/registrar-reciclaje", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    botella_detectada: resultadoAnalisis.botella_detectada,
                    tapa_detectada: resultadoAnalisis.tapa_detectada,
                    etiqueta_detectada: resultadoAnalisis.etiqueta_detectada,
                    confianza: resultadoAnalisis.confianza,
                    puntos_base: resultadoAnalisis.puntos_base,
                    puntos_tapa: resultadoAnalisis.puntos_tapa,
                    puntos_etiqueta: resultadoAnalisis.puntos_etiqueta,
                    puntos: resultadoAnalisis.puntos
                }),
                credentials: "same-origin"
            });

            var contentType = response.headers.get("content-type") || "";
            if (contentType.indexOf("application/json") === -1) {
                throw new Error("El servidor no respondi\u00f3 correctamente. Intenta de nuevo en unos segundos.");
            }

            var data = await response.json();
            console.log("RESPUESTA REGISTRO:", data);
            isProcessing = false;

            if (!response.ok) {
                throw new Error(data.error || "Error registrando el reciclaje.");
            }

            if (currentPoints && data.saldo_nuevo !== undefined) {
                currentPoints.textContent = data.saldo_nuevo;
            }

            hideElement(scanResult);

            await showModal({
                type: "success",
                title: "\u00a1Botella registrada!",
                text: "Tu botella fue registrada correctamente y los SIGIPUNTOS fueron asignados a tu cuenta.",
                points: data.puntos || 0,
                comprobante: data.numero_comprobante || "",
                buttonText: "ACEPTAR"
            });

            window.location.href = dashboardUrl;

        } catch (error) {
            console.error("ERROR RECICLANDO:", error);
            isProcessing = false;
            recycleButton.disabled = false;
            recycleButton.innerHTML = "<span>\u267B RECICLAR</span>";

            await showModal({
                type: "error",
                title: "Error al registrar",
                text: error.message || "No fue posible registrar el reciclaje. Intenta de nuevo.",
                buttonText: "REINTENTAR"
            });
        }
    });


    // =====================================================
    // DETENER CÁMARA AL SALIR
    // =====================================================

    window.addEventListener("beforeunload", function() {
        if (stream) {
            stream.getTracks().forEach(function(track) { track.stop(); });
        }
    });

});
