/* =====================================================================
 * api.js — Cliente HTTP para consumir la API REST con fetch
 * ===================================================================== */
"use strict";

const API = (() => {
  // Si el frontend vive en otro dominio, define window.API_BASE antes de cargar.
  const BASE = (window.API_BASE || "").trim().replace(/\/+$/, "");

  async function request(method, path, body) {
    const opciones = {
      method,
      headers: { "Content-Type": "application/json" },
    };
    if (body !== undefined) {
      opciones.body = JSON.stringify(body);
    }

    let respuesta;
    try {
      respuesta = await fetch(BASE + path, opciones);
    } catch {
      throw new Error("No se pudo conectar con el servidor. Revisa tu conexión.");
    }

    let datos = null;
    try {
      datos = await respuesta.json();
    } catch {
      datos = null;
    }

    if (!respuesta.ok) {
      const mensaje = datos && (datos.error || datos.mensaje) ? (datos.error || datos.mensaje) : "Ocurrió un error inesperado.";
      throw new Error(mensaje);
    }

    if (!datos) return null;

    // Retorna .datos (Flask/PHP estándar), .data (REST genérico) o el objeto completo si viene en la raíz
    return datos.datos !== undefined ? datos.datos : (datos.data !== undefined ? datos.data : datos);
  }

  return {
    get: (p) => request("GET", p),
    post: (p, b) => request("POST", p, b),
    put: (p, b) => request("PUT", p, b),
    del: (p) => request("DELETE", p),
  };
})();

/* =====================================================================
 * Sesión guardada en localStorage
 * ===================================================================== */
const Sesion = (() => {
  const LLAVE = "finanzas_usuario";

  return {
    guardar(usuario) {
      try {
        localStorage.setItem(LLAVE, JSON.stringify(usuario));
      } catch {
        sessionStorage.setItem(LLAVE, JSON.stringify(usuario));
      }
    },
    actual() {
      try {
        return JSON.parse(localStorage.getItem(LLAVE) || sessionStorage.getItem(LLAVE) || "null");
      } catch {
        return null;
      }
    },
    cerrar() {
      localStorage.removeItem(LLAVE);
      sessionStorage.removeItem(LLAVE);
    },
  };
})();

/* =====================================================================
 * Utilidades de formato
 * ===================================================================== */
const Formato = {
  moneda(importe) {
    return new Intl.NumberFormat("es-CO", {
      style: "currency",
      currency: "COP",
      maximumFractionDigits: 0,
    }).format(importe || 0);
  },

  fecha(fecha) {
    if (!fecha) return "—";
    const [anio, mes, dia] = String(fecha).slice(0, 10).split("-");
    if (!anio || !mes || !dia) return fecha;
    return `${dia}/${mes}/${anio}`;
  },

  hoy() {
    const d = new Date();
    const mes = String(d.getMonth() + 1).padStart(2, "0");
    const dia = String(d.getDate()).padStart(2, "0");
    return `${d.getFullYear()}-${mes}-${dia}`;
  },

  inicial(nombre) {
    return String(nombre || "?").trim().charAt(0).toUpperCase() || "?";
  },
};