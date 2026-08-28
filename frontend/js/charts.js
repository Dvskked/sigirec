/* =====================================================================
 * charts.js — Wrappers de Chart.js para los gráficos del dashboard
 * ===================================================================== */
"use strict";

const Graficos = (() => {
  const PALETA = [
    "#4f46e5", "#ef4444", "#f59e0b", "#10b981", "#0ea5e9",
    "#8b5cf6", "#ec4899", "#14b8a6", "#f97316", "#64748b",
  ];

  let graficoDona = null;
  let graficoLinea = null;

  function disponibles() {
    return typeof Chart !== "undefined";
  }

  function actualizarDona(canvas, datos) {
    const etiquetas = datos.map((d) => d.categoria);
    const valores = datos.map((d) => d.total);

    if (graficoDona) {
      graficoDona.data.labels = etiquetas;
      graficoDona.data.datasets[0].data = valores;
      graficoDona.update();
      return;
    }

    graficoDona = new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: etiquetas,
        datasets: [
          {
            data: valores,
            backgroundColor: PALETA,
            borderColor: "#ffffff",
            borderWidth: 2,
            hoverOffset: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { boxWidth: 14, font: { size: 11 } } },
          tooltip: {
            callbacks: {
              label: (ctx) => {
                const total = ctx.dataset.data.reduce((a, b) => a + b, 0) || 1;
                const porcentaje = ((ctx.parsed / total) * 100).toFixed(1);
                return ` ${ctx.label}: ${Formato.moneda(ctx.parsed)} (${porcentaje}%)`;
              },
            },
          },
        },
      },
    });
  }

  function actualizarLinea(canvas, series) {
    const meses = series.map((s) => s.mes);
    const ingresos = series.map((s) => s.ingresos);
    const gastos = series.map((s) => s.gastos);

    if (graficoLinea) {
      graficoLinea.data.labels = meses;
      graficoLinea.data.datasets[0].data = ingresos;
      graficoLinea.data.datasets[1].data = gastos;
      graficoLinea.update();
      return;
    }

    graficoLinea = new Chart(canvas, {
      type: "line",
      data: {
        labels: meses,
        datasets: [
          {
            label: "Ingresos",
            data: ingresos,
            borderColor: "#16a34a",
            backgroundColor: "rgba(22, 163, 74, 0.12)",
            fill: true,
            tension: 0.35,
            pointRadius: 4,
            borderWidth: 2,
          },
          {
            label: "Gastos",
            data: gastos,
            borderColor: "#dc2626",
            backgroundColor: "rgba(220, 38, 38, 0.10)",
            fill: true,
            tension: 0.35,
            pointRadius: 4,
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { position: "bottom", labels: { boxWidth: 14, font: { size: 11 } } },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.dataset.label}: ${Formato.moneda(ctx.parsed.y)}`,
            },
          },
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            beginAtZero: true,
            ticks: { callback: (v) => Formato.moneda(v) },
          },
        },
      },
    });
  }

  function vaciar() {
    if (graficoDona) { graficoDona.destroy(); graficoDona = null; }
    if (graficoLinea) { graficoLinea.destroy(); graficoLinea = null; }
  }

  return { disponibles, actualizarDona, actualizarLinea, vaciar };
})();