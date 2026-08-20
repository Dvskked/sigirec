document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // ELEMENTOS
    // =====================================================

    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");

    const startCameraButton =
        document.getElementById("start-camera");

    const takePhotoButton =
        document.getElementById("take-photo");

    const cameraPlaceholder =
        document.getElementById("camera-placeholder");

    const scanFrame =
        document.getElementById("scan-frame");

    const scanLine =
        document.getElementById("scan-line");

    const scanResult =
        document.getElementById("scan-result");

    const scanLoading =
        document.getElementById("scan-loading");

    const resultTitle =
        document.getElementById("result-title");

    const resultDescription =
        document.getElementById("result-description");

    const resultPoints =
        document.getElementById("result-points-value");

    const resultImage =
        document.getElementById("result-image");

    const recycleButton =
        document.getElementById("recycle-button");

    const currentPoints =
        document.getElementById("current-points");

    const aiStatusText =
        document.getElementById("ai-status-text");

    const aiStatus =
        document.getElementById("ai-status");

    const detectionDetails =
        document.getElementById("detection-details");

    const retryMessage =
        document.getElementById("retry-message");

    const cameraWrapper =
        document.querySelector(".camera-wrapper");

    const cameraControls =
        document.querySelector(".camera-controls");

    const scannerHelp =
        document.querySelector(".scanner-help");

    const scanPage =
        document.querySelector(".scan-page");


    // =====================================================
    // MODAL
    // =====================================================

    const modalOverlay =
        document.getElementById("sigi-modal-overlay");

    const modalIcon =
        document.getElementById("sigi-modal-icon");

    const modalTitle =
        document.getElementById("sigi-modal-title");

    const modalText =
        document.getElementById("sigi-modal-text");

    const modalPoints =
        document.getElementById("sigi-modal-points");

    const modalPointsValue =
        document.getElementById("sigi-modal-points-value");

    const modalComprobante =
        document.getElementById("sigi-modal-comprobante");

    const modalCompNum =
        document.getElementById("sigi-modal-comp-num");

    const modalBtn =
        document.getElementById("sigi-modal-btn");


    // =====================================================
    // VARIABLES
    // =====================================================

    let stream = null;
    let cameraActive = false;
    let resultadoAnalisis = null;
    let isProcessing = false;

    const dashboardUrl =
        scanPage
            ? scanPage.getAttribute("data-dashboard-url")
            : "/dashboard";


    // =====================================================
    // FUNCIONES AUXILIARES
    // =====================================================

    function showElement(el) {
        if (!el) return;
        el.style.display = "";
    }


    function hideElement(el) {
        if (!el) return;
        el.style.display = "none";
    }


    function stopCamera() {
        if (stream) {
            stream
                .getTracks()
                .forEach(track => track.stop());
            stream = null;
        }
        cameraActive = false;
    }


    function resetUI() {
        hideElement(scanResult);
        hideElement(scanLoading);

        if (retryMessage) {
            retryMessage.style.display = "none";
        }

        if (detectionDetails) {
            detectionDetails.style.display = "none";
            detectionDetails.innerHTML = "";
        }

        if (recycleButton) {
            recycleButton.style.display = "none";
            recycleButton.disabled = false;
            recycleButton.innerHTML = "<span>♻ RECICLAR</span>";
        }
    }


    function showModal(config) {

        if (!modalOverlay) return;

        modalIcon.className =
            "sigi-modal-icon " +
            (config.type || "success");

        modalIcon.textContent =
            config.type === "error" ? "✕" : "♻";

        modalTitle.textContent =
            config.title || "";

        modalText.textContent =
            config.text || "";

        if (config.points !== undefined) {

            modalPoints.style.display = "";
            modalPointsValue.textContent =
                config.points;

        } else {

            modalPoints.style.display = "none";

        }

        if (config.comprobante) {

            modalComprobante.style.display = "";
            modalCompNum.textContent =
                config.comprobante;

        } else {

            modalComprobante.style.display = "none";

        }

        modalBtn.className =
            "sigi-modal-btn" +
            (config.type === "error"
                ? " error-btn"
                : "");

        modalBtn.textContent =
            config.buttonText || "ACEPTAR";

        modalOverlay.classList.add("visible");

        return new Promise((resolve) => {

            const handler = () => {

                modalOverlay.classList.remove("visible");

                modalBtn.removeEventListener(
                    "click",
                    handler
                );

                resolve();

            };

            modalBtn.addEventListener(
                "click",
                handler
            );

        });

    }


    function buildDetectionHTML(detecciones) {

        if (
            !detecciones ||
            detecciones.length === 0
        ) {
            return "";
        }

        let html = "";

        const iconMap = {
            "botella": "♻",
            "tapa": "◉",
            "etiqueta": "▤"
        };

        detecciones.forEach((det) => {

            const icon =
                iconMap[det.clase] || "●";

            const conf =
                (det.confianza * 100)
                    .toFixed(1);

            html +=
                '<div class="detection-item">' +
                    "<span>" + icon + "</span>" +
                    "<strong>" +
                        det.clase.toUpperCase() +
                    "</strong>" +
                    "<span>" + conf + "%</span>" +
                "</div>";

        });

        return html;

    }


    // =====================================================
    // ACTIVAR CÁMARA
    // =====================================================

    startCameraButton.addEventListener(
        "click",
        async () => {

            if (cameraActive && stream) {
                return;
            }

            resetUI();

            try {

                startCameraButton.disabled = true;

                startCameraButton.innerHTML =
                    '<span class="button-icon">◌</span>' +
                    "<span>Activando cámara...</span>";

                stream =
                    await navigator
                        .mediaDevices
                        .getUserMedia({

                            video: {
                                width: {
                                    ideal: 1280
                                },
                                height: {
                                    ideal: 720
                                },
                                facingMode: "user"
                            },

                            audio: false

                        });

                video.srcObject = stream;
                video.style.display = "block";

                hideElement(cameraPlaceholder);

                await new Promise((resolve) => {

                    if (video.readyState >= 2) {
                        resolve();
                    } else {
                        video.onloadedmetadata =
                            () => resolve();
                    }

                });

                try {
                    await video.play();
                } catch (e) {
                    console.warn(
                        "Video play:",
                        e
                    );
                }

                cameraActive = true;

                takePhotoButton.disabled = false;

                startCameraButton.innerHTML =
                    '<span class="button-icon">✓</span>' +
                    "<span>Cámara activa</span>";

                if (aiStatusText) {
                    aiStatusText.textContent =
                        "Cámara activa";
                }

                if (aiStatus) {
                    aiStatus.classList.add("active");
                }

                showElement(scanFrame);
                showElement(scanLine);

            } catch (error) {

                console.error(
                    "ERROR CÁMARA:",
                    error
                );

                cameraActive = false;
                stream = null;

                startCameraButton.disabled = false;

                startCameraButton.innerHTML =
                    '<span class="button-icon">⌁</span>' +
                    "<span>Escanear botella</span>";

                let msg =
                    "No fue posible activar la cámara.";

                if (
                    error.name === "NotAllowedError"
                ) {
                    msg =
                        "Permiso de cámara denegado. " +
                        "Permite el acceso a la cámara " +
                        "desde el navegador.";
                }
                else if (
                    error.name === "NotFoundError"
                ) {
                    msg =
                        "No se encontró ninguna cámara.";
                }
                else if (
                    error.name === "NotReadableError"
                ) {
                    msg =
                        "La cámara está siendo utilizada " +
                        "por otra aplicación.";
                }

                await showModal({
                    type: "error",
                    title: "Error de cámara",
                    text: msg,
                    buttonText: "ENTENDIDO"
                });

            }

        }
    );


    // =====================================================
    // TOMAR FOTO
    // =====================================================

    takePhotoButton.addEventListener(
        "click",
        async () => {

            if (
                !stream ||
                !cameraActive ||
                video.readyState < 2
            ) {

                await showModal({
                    type: "error",
                    title: "Cámara inactiva",
                    text:
                        "Primero debes activar la cámara.",
                    buttonText: "ENTENDIDO"
                });

                return;

            }

            if (isProcessing) return;

            const width =
                video.videoWidth;

            const height =
                video.videoHeight;

            if (width === 0 || height === 0) {

                await showModal({
                    type: "error",
                    title: "Cámara no lista",
                    text:
                        "La cámara todavía no está lista. " +
                        "Espera un momento e inténtalo.",
                    buttonText: "ENTENDIDO"
                });

                return;

            }


            // =========================================
            // CAPTURAR FOTO
            // =========================================

            canvas.width = width;
            canvas.height = height;

            const ctx =
                canvas.getContext("2d");

            ctx.drawImage(
                video,
                0,
                0,
                width,
                height
            );


            // =========================================
            // PREPARAR ENVÍO
            // =========================================

            const fotoCapturada =
                canvas.toDataURL(
                    "image/jpeg",
                    0.90
                );

            if (resultImage) {
                resultImage.src = fotoCapturada;
            }

            resetUI();
            hideElement(scanResult);

            showElement(scanLoading);

            takePhotoButton.disabled = true;
            startCameraButton.disabled = true;

            isProcessing = true;


            canvas.toBlob(
                async (blob) => {

                    isProcessing = false;

                    if (!blob) {

                        hideElement(scanLoading);

                        takePhotoButton.disabled =
                            false;

                        startCameraButton.disabled =
                            false;

                        await showModal({
                            type: "error",
                            title: "Error",
                            text:
                                "No fue posible capturar la imagen.",
                            buttonText: "ENTENDIDO"
                        });

                        return;

                    }


                    // =================================
                    // ENVIAR A FLASK
                    // =================================

                    const formData =
                        new FormData();

                    formData.append(
                        "imagen",
                        blob,
                        "reciclaje.jpg"
                    );

                    try {

                        const response =
                            await fetch(
                                "/api/escanear",
                                {
                                    method: "POST",
                                    body: formData,
                                    credentials: "same-origin"
                                }
                            );

                        const contentType =
                            response.headers
                                .get("content-type") || "";

                        if (
                            !contentType
                                .includes("application/json")
                        ) {

                            throw new Error(
                                "El servidor no respondió correctamente. " +
                                "Intenta de nuevo en unos segundos."
                            );

                        }

                        const data =
                            await response.json();

                        console.log(
                            "RESPUESTA API:",
                            data
                        );


                        if (!response.ok) {

                            throw new Error(
                                data.error ||
                                "Error procesando la imagen."
                            );

                        }


                        resultadoAnalisis = data;

                        hideElement(scanLoading);


                        // =============================
                        // IMAGEN YOLO
                        // =============================

                        if (
                            data.imagen &&
                            resultImage
                        ) {

                            resultImage.src =
                                "data:image/jpeg;base64," +
                                data.imagen;

                        }


                        // =============================
                        // BOTELLA DETECTADA
                        // =============================

                        if (
                            data.success &&
                            data.botella_detectada
                        ) {

                            stopCamera();

                            hideElement(cameraWrapper);
                            hideElement(cameraControls);
                            hideElement(scannerHelp);

                            resultTitle.textContent =
                                data.titulo ||
                                "¡Botella reconocida!";

                            resultDescription.textContent =
                                data.mensaje ||
                                "La botella fue reconocida correctamente.";

                            resultPoints.textContent =
                                data.puntos || 0;

                            if (
                                detectionDetails &&
                                data.detecciones
                            ) {

                                const html =
                                    buildDetectionHTML(
                                        data.detecciones
                                    );

                                if (html) {

                                    detectionDetails.innerHTML =
                                        html;

                                    showElement(
                                        detectionDetails
                                    );

                                }

                            }

                            if (retryMessage) {
                                retryMessage.style.display =
                                    "none";
                            }

                            if (recycleButton) {
                                showElement(
                                    recycleButton
                                );
                            }

                            showElement(scanResult);

                            return;

                        }


                        // =============================
                        // NO SE DETECTÓ BOTELLA
                        // =============================

                        resultTitle.textContent =
                            data.titulo ||
                            "Botella no reconocida";

                        resultDescription.textContent =
                            data.mensaje ||
                            "No se detectó una botella válida.";

                        resultPoints.textContent = "0";

                        if (recycleButton) {
                            recycleButton.style.display =
                                "none";
                        }

                        if (retryMessage) {
                            showElement(retryMessage);
                        }

                        showElement(scanResult);

                        takePhotoButton.disabled =
                            false;

                        startCameraButton.disabled =
                            true;

                        startCameraButton.innerHTML =
                            '<span class="button-icon">✓</span>' +
                            "<span>Cámara activa</span>";


                    } catch (error) {

                        console.error(
                            "ERROR ANALIZANDO:",
                            error
                        );

                        hideElement(scanLoading);

                        resultTitle.textContent =
                            "Error en el análisis";

                        resultDescription.textContent =
                            error.message;

                        resultPoints.textContent = "0";

                        if (recycleButton) {
                            recycleButton.style.display =
                                "none";
                        }

                        if (retryMessage) {
                            showElement(retryMessage);
                        }

                        showElement(scanResult);

                        takePhotoButton.disabled =
                            false;

                        startCameraButton.disabled =
                            true;

                        startCameraButton.innerHTML =
                            '<span class="button-icon">✓</span>' +
                            "<span>Cámara activa</span>";

                    }

                },

                "image/jpeg",
                0.90

            );

        }
    );


    // =====================================================
    // BOTÓN RECICLAR
    // =====================================================

    recycleButton.addEventListener(
        "click",
        async () => {

            if (
                !resultadoAnalisis ||
                !resultadoAnalisis.botella_detectada
            ) {
                return;
            }

            if (isProcessing) return;

            isProcessing = true;

            recycleButton.disabled = true;

            recycleButton.innerHTML =
                '<span class="button-spinner"></span>' +
                "<span>Procesando...</span>";

            try {

                const response =
                    await fetch(
                        "/api/registrar-reciclaje",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body: JSON.stringify({
                                botella_detectada:
                                    resultadoAnalisis.botella_detectada,
                                tapa_detectada:
                                    resultadoAnalisis.tapa_detectada,
                                etiqueta_detectada:
                                    resultadoAnalisis.etiqueta_detectada,
                                confianza:
                                    resultadoAnalisis.confianza,
                                puntos_base:
                                    resultadoAnalisis.puntos_base,
                                puntos_tapa:
                                    resultadoAnalisis.puntos_tapa,
                                puntos_etiqueta:
                                    resultadoAnalisis.puntos_etiqueta,
                                puntos:
                                    resultadoAnalisis.puntos
                            }),
                            credentials: "same-origin"
                        }
                    );

                const contentType =
                    response.headers
                        .get("content-type") || "";

                if (
                    !contentType
                        .includes("application/json")
                ) {

                    throw new Error(
                        "El servidor no respondió correctamente. " +
                        "Intenta de nuevo en unos segundos."
                    );

                }

                const data =
                    await response.json();

                console.log(
                    "RESPUESTA REGISTRO:",
                    data
                );

                isProcessing = false;


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Error registrando el reciclaje."
                    );

                }


                // =============================
                // ÉXITO - MOSTRAR MODAL
                // =============================

                if (currentPoints && data.saldo_nuevo !== undefined) {
                    currentPoints.textContent =
                        data.saldo_nuevo;
                }

                hideElement(scanResult);

                await showModal({
                    type: "success",
                    title: "¡Botella registrada!",
                    text:
                        "Tu botella fue registrada correctamente " +
                        "y los SIGIPUNTOS fueron asignados a tu cuenta.",
                    points: data.puntos || 0,
                    comprobante:
                        data.numero_comprobante || "",
                    buttonText: "ACEPTAR"
                });

                window.location.href =
                    dashboardUrl;


            } catch (error) {

                console.error(
                    "ERROR RECICLANDO:",
                    error
                );

                isProcessing = false;

                recycleButton.disabled = false;

                recycleButton.innerHTML =
                    "<span>♻ RECICLAR</span>";

                await showModal({
                    type: "error",
                    title: "Error al registrar",
                    text:
                        error.message ||
                        "No fue posible registrar el reciclaje. Intenta de nuevo.",
                    buttonText: "REINTENTAR"
                });

            }

        }
    );


    // =====================================================
    // DETENER CÁMARA AL SALIR
    // =====================================================

    window.addEventListener(
        "beforeunload",
        () => {

            if (stream) {

                stream
                    .getTracks()
                    .forEach(
                        track => track.stop()
                    );

            }

        }
    );

});
