/* =====================================================================
 * app.js — Controlador principal del dashboard (Corregido)
 * ===================================================================== */
"use strict";

(() => {
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const Estado = {
    usuario: null,
    categorias: [],
    editandoMovimientoId: null,
  };

  /* ------------------------- Utilidades UI ------------------------- */
  let toastTimer = null;
  function toast(mensaje, tipo = "exito", ms = 3800) {
    const el = $("#toast");
    el.textContent = mensaje;
    el.className = `toast toast--${tipo}`;
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      el.hidden = true;
    }, ms);
  }

  function cargando(activo) {
    $("#vista-app").classList.toggle("cargando", activo);
  }

  /* ------------------------- Vistas ------------------------- */
  function mostrarAuth() {
    $("#vista-auth").hidden = false;
    $("#vista-app").hidden = true;
    $("#cabecera-usuario").hidden = true;
  }

  function mostrarApp() {
    $("#vista-auth").hidden = true;
    $("#vista-app").hidden = false;
    $("#cabecera-usuario").hidden = false;

    // Normalizar Estado.usuario en caso de venir anidado desde backend/localStorage
    if (Estado.usuario && Estado.usuario.datos) {
      Estado.usuario = Estado.usuario.datos;
    }

    const u = Estado.usuario || {};
    const nombre = u.nombre || "Usuario";

    $("#usuario-nombre").textContent = nombre;
    $("#usuario-correo").textContent = u.correo || "";
    $("#avatar-inicial").textContent = Formato.inicial(nombre);
    $("#bienvenida-nombre").textContent = nombre.split(" ")[0];

    cargarDashboard();
  }

  /* ------------------------- Dashboard ------------------------- */
  async function cargarDashboard() {
    cargando(true);
    try {
      const datos = await API.get(`/api/dashboard?id_usuario=${Estado.usuario.id_usuario}`);
      Estado.categorias = datos.categorias || [];
      renderizarDashboard(datos);
    } catch (error) {
      toast(error.message, "error");
    } finally {
      cargando(false);
    }
  }

  function renderizarDashboard(datos) {
    const t = datos.totales;
    $("#kpi-ingresos").textContent = Formato.moneda(t.total_ingresos);
    $("#kpi-gastos").textContent = Formato.moneda(t.total_gastos);
    $("#kpi-balance").textContent = Formato.moneda(t.balance);

    const prevision = datos.prediccion || {};
    $("#kpi-prediccion").textContent =
      prevision.prediccion_proximo_mes != null
        ? Formato.moneda(prevision.prediccion_proximo_mes)
        : "—";
    $("#kpi-prediccion-detalle").textContent =
      prevision.mensaje || (prevision.metodo ? `Método: ${prevision.metodo}` : "");

    renderizarGraficos(datos);
    renderizarAnomalias(datos.anomalias);
    renderizarCategorias();
    renderizarMovimientos(datos.recientes);
  }

  function renderizarGraficos(datos) {
    if (!Graficos.disponibles()) {
      $("#grafico-dona").style.display = "none";
      $("#grafico-linea").style.display = "none";
      const conts = $$(".grafico-contenedor");
      conts.forEach((c) => {
        if (!c.querySelector(".grafico-error")) {
          const p = document.createElement("p");
          p.className = "grafico-error";
          p.textContent = "No se pudo cargar Chart.js. Verifica tu conexión.";
          c.appendChild(p);
        }
      });
      return;
    }
    Graficos.actualizarDona($("#grafico-dona"), datos.por_categoria || []);
    Graficos.actualizarLinea($("#grafico-linea"), datos.series_mensuales || []);
  }

  function renderizarAnomalias(anomalias) {
    const lista = $("#alerta-lista");
    const vacia = $("#alerta-vacia");
    lista.innerHTML = "";

    if (!anomalias || anomalias.length === 0) {
      vacia.hidden = false;
      return;
    }
    vacia.hidden = true;

    anomalias.forEach((a) => {
      const li = document.createElement("li");
      li.className = "alerta-item";

      const info = document.createElement("div");
      const titulo = document.createElement("strong");
      titulo.textContent = `${a.categoria}: ${Formato.moneda(a.monto)}`;
      const meta = document.createElement("div");
      meta.className = "alerta-item__meta";
      meta.textContent =
        `${Formato.fecha(a.fecha)} · ${a.motivo} · Z = ${a.z_score} ` +
        `(promedio de categoría: ${Formato.moneda(a.promedio_categoria)})`;

      info.appendChild(titulo);
      info.appendChild(meta);
      li.appendChild(info);
      lista.appendChild(li);
    });
  }

  /* ------------------------- Categorías ------------------------- */
  function renderizarCategorias() {
    const lista = $("#chip-lista-categorias");
    lista.innerHTML = "";

    Estado.categorias.forEach((cat) => {
      const li = document.createElement("li");
      li.className = `chip chip--${cat.tipo}`;

      const span = document.createElement("span");
      span.textContent = `${cat.nombre} (${cat.tipo})`;

      const btn = document.createElement("button");
      btn.type = "button";
      btn.setAttribute("aria-label", `Eliminar categoría ${cat.nombre}`);
      btn.textContent = "×";
      btn.addEventListener("click", () => eliminarCategoria(cat));

      li.appendChild(span);
      li.appendChild(btn);
      lista.appendChild(li);
    });

    llenarSelectCategorias();
  }

  async function eliminarCategoria(cat) {
    if (!window.confirm(`¿Eliminar la categoría "${cat.nombre}"?`)) return;
    try {
      await API.del(
        `/api/categorias/${cat.id_categoria}?id_usuario=${Estado.usuario.id_usuario}`
      );
      toast(`Categoría "${cat.nombre}" eliminada.`);
      await cargarDashboard();
    } catch (error) {
      toast(error.message, "error", 5000);
    }
  }

  function llenarSelectCategorias() {
    const select = $("#mov-categoria");
    const tipo = $("#mov-tipo").value;
    const actual = select.value;

    const opciones = Estado.categorias.filter((c) => c.tipo === tipo);
    select.innerHTML = "";
    opciones.forEach((c) => {
      const op = document.createElement("option");
      op.value = c.id_categoria;
      op.textContent = c.nombre;
      select.appendChild(op);
    });

    if (opciones.some((c) => String(c.id_categoria) === actual)) {
      select.value = actual;
    }
  }

  /* ------------------------- Movimientos ------------------------- */
  function renderizarMovimientos(recientes) {
    const cuerpo = $("#tabla-movimientos-cuerpo");
    const vacia = $("#tabla-vacia");
    cuerpo.innerHTML = "";

    if (!recientes || recientes.length === 0) {
      vacia.hidden = false;
      $("#tabla-movimientos").style.display = "none";
      return;
    }
    vacia.hidden = true;
    $("#tabla-movimientos").style.display = "";

    recientes.forEach((m) => {
      const tr = document.createElement("tr");

      const tdFecha = document.createElement("td");
      tdFecha.textContent = Formato.fecha(m.fecha);

      const tdCat = document.createElement("td");
      const badge = document.createElement("span");
      badge.className = `badge badge-tipo badge-tipo--${m.tipo}`;
      badge.textContent = m.tipo;
      tdCat.append(
        `${m.categoria} `,
        badge
      );

      const tdDesc = document.createElement("td");
      tdDesc.textContent = m.descripcion || "—";

      const tdMonto = document.createElement("td");
      tdMonto.className = `tabla__monto monto-${m.tipo}`;
      tdMonto.textContent = Formato.moneda(m.monto);

      const tdAcc = document.createElement("td");
      tdAcc.className = "tabla__acciones";

      const btnEditar = document.createElement("button");
      btnEditar.type = "button";
      btnEditar.className = "btn btn-secundario btn-pequeno";
      btnEditar.textContent = "Editar";
      btnEditar.addEventListener("click", () => editarMovimiento(m));

      const btnEliminar = document.createElement("button");
      btnEliminar.type = "button";
      btnEliminar.className = "btn btn-peligro btn-pequeno";
      btnEliminar.textContent = "Borrar";
      btnEliminar.addEventListener("click", () => eliminarMovimiento(m));

      tdAcc.append(btnEditar, " ", btnEliminar);

      tr.append(tdFecha, tdCat, tdDesc, tdMonto, tdAcc);
      cuerpo.appendChild(tr);
    });
  }

  function editarMovimiento(m) {
    Estado.editandoMovimientoId = m.id_movimiento;
    $("#mov-tipo").value = m.tipo;
    $("#mov-monto").value = m.monto;
    $("#mov-fecha").value = String(m.fecha).slice(0, 10);
    $("#mov-descripcion").value = m.descripcion || "";
    $("#titulo-formulario").textContent = "Editar transacción";
    $("#btn-guardar-movimiento").textContent = "Actualizar";
    $("#btn-cancelar-edicion").hidden = false;
    $("#mov-categoria").value = m.id_categoria;
    llenarSelectCategorias();
    if (Array.from($("#mov-categoria").options).every((o) => o.value !== String(m.id_categoria))) {
      $("#mov-categoria").value = "";
    }
    $("#form-movimiento").scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function cancelarEdicion() {
    Estado.editandoMovimientoId = null;
    $("#form-movimiento").reset();
    $("#mov-fecha").value = Formato.hoy();
    $("#titulo-formulario").textContent = "Nueva transacción";
    $("#btn-guardar-movimiento").textContent = "Guardar";
    $("#btn-cancelar-edicion").hidden = true;
    llenarSelectCategorias();
  }

  async function eliminarMovimiento(m) {
    if (!window.confirm("¿Eliminar este movimiento?")) return;
    try {
      await API.del(
        `/api/movimientos/${m.id_movimiento}?id_usuario=${Estado.usuario.id_usuario}`
      );
      toast("Movimiento eliminado.");
      await cargarDashboard();
    } catch (error) {
      toast(error.message, "error");
    }
  }

  /* ------------------------- Eventos ------------------------- */
  function enlazarEventos() {
    // Autenticación
    $("#form-login").addEventListener("submit", iniciarSesion);
    $("#form-registro").addEventListener("submit", registrarUsuario);
    $("#btn-mostrar-registro").addEventListener("click", () => {
      $("#tarjeta-login").hidden = true;
      $("#tarjeta-registro").hidden = false;
    });
    $("#btn-mostrar-login").addEventListener("click", () => {
      $("#tarjeta-login").hidden = false;
      $("#tarjeta-registro").hidden = true;
    });
    $("#btn-cerrar-sesion").addEventListener("click", cerrarSesion);

    // Dashboard
    $("#form-movimiento").addEventListener("submit", guardarMovimiento);
    $("#btn-cancelar-edicion").addEventListener("click", cancelarEdicion);
    $("#form-categoria").addEventListener("submit", agregarCategoria);
    $("#mov-tipo").addEventListener("change", llenarSelectCategorias);
  }

 async function iniciarSesion(evento) {
    evento.preventDefault();
    const correo = $("#login-correo").value.trim();
    const contrasena = $("#login-contrasena").value;

    try {
      const respuesta = await API.post("/api/usuarios/login", { correo, contrasena });

      if (!respuesta) {
        throw new Error("No se obtuvo respuesta del servidor.");
      }

      // Acceso seguro usando ?.
      const usuario = respuesta?.datos || respuesta?.usuario || respuesta;

      if (!usuario || (!usuario.id_usuario && !usuario.nombre)) {
        throw new Error("Credenciales inválidas o respuesta malformada.");
      }

      Estado.usuario = usuario;
      Sesion.guardar(usuario);
      toast(`Bienvenido/a, ${usuario.nombre ? usuario.nombre.split(" ")[0] : "Usuario"}.`);
      mostrarApp();
      evento.target.reset();
    } catch (error) {
      toast(error.message || "Error al iniciar sesión", "error");
    }
  }

  async function registrarUsuario(evento) {
    evento.preventDefault();
    const cuerpo = {
      nombre: $("#reg-nombre").value.trim(),
      correo: $("#reg-correo").value.trim(),
      contrasena: $("#reg-contrasena").value,
    };

    try {
      const respuesta = await API.post("/api/usuarios", cuerpo);

      if (!respuesta) {
        throw new Error("No se obtuvo respuesta del servidor.");
      }

      // Acceso seguro usando ?.
      const usuario = respuesta?.datos || respuesta?.usuario || respuesta;

      if (!usuario || (!usuario.id_usuario && !usuario.nombre)) {
        throw new Error("No se pudo crear la cuenta.");
      }

      Estado.usuario = usuario;
      Sesion.guardar(usuario);
      toast("Cuenta creada correctamente.");
      mostrarApp();
      evento.target.reset();
    } catch (error) {
      toast(error.message || "Error al registrar usuario", "error");
    }
  }

  function mostrarApp() {
    $("#vista-auth").hidden = true;
    $("#vista-app").hidden = false;
    $("#cabecera-usuario").hidden = false;

    // Normalización segura
    if (Estado.usuario?.datos) {
      Estado.usuario = Estado.usuario.datos;
    }

    const u = Estado.usuario || {};
    const nombre = u.nombre || "Usuario";

    $("#usuario-nombre").textContent = nombre;
    $("#usuario-correo").textContent = u.correo || "";
    $("#avatar-inicial").textContent = Formato.inicial(nombre);
    $("#bienvenida-nombre").textContent = nombre.split(" ")[0];

    cargarDashboard();
  }

  function inicio() {
    enlazarEventos();

    let usuario = Sesion.actual();
    if (usuario) {
      if (usuario?.datos) usuario = usuario.datos;
      Estado.usuario = usuario;
      mostrarApp();
    } else {
      mostrarAuth();
    }
  }

  document.addEventListener("DOMContentLoaded", inicio);
})();