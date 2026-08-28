"""Utilidades de agregación financiera con Pandas.

Convierte los movimiento (listas de diccionarios) en series temporales
mensuales, distribución por categoría y resúmenes de KPIs.
"""

import pandas as pd


def _dataframe_movimientos(movimientos):
    df = pd.DataFrame(movimientos or [])
    if df.empty:
        return df
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    df["monto"] = df["monto"].astype(float)
    return df


def resumen_totales(movimientos):
    """Devuelve totales de ingresos, gastos y balance neto."""
    df = _dataframe_movimientos(movimientos)
    total_ingresos = float(df.loc[df["tipo"] == "ingreso", "monto"].sum()) if not df.empty else 0.0
    total_gastos = float(df.loc[df["tipo"] == "gasto", "monto"].sum()) if not df.empty else 0.0
    return {
        "total_ingresos": round(total_ingresos, 2),
        "total_gastos": round(total_gastos, 2),
        "balance": round(total_ingresos - total_gastos, 2),
    }


def distribucion_por_categoria(movimientos):
    """Gasto total agrupado por categoría (para el gráfico de dona)."""
    df = _dataframe_movimientos(movimientos)
    if df.empty:
        return []
    gastos = df[df["tipo"] == "gasto"]
    if gastos.empty:
        return []
    agrupado = (
        gastos.groupby(["id_categoria", "categoria"], as_index=False)["monto"]
        .sum()
        .sort_values("monto", ascending=False)
    )
    return [
        {"id_categoria": int(r.id_categoria), "categoria": r.categoria,
         "total": round(float(r.monto), 2)}
        for r in agrupado.itertuples(index=False)
    ]


def series_mensuales(movimientos):
    """Ingresos y gastos agregados por mes (para el gráfico de líneas)."""
    df = _dataframe_movimientos(movimientos)
    if df.empty:
        return []
    tabla = (
        df.groupby(["mes", "tipo"], as_index=False)["monto"]
        .sum()
        .pivot(index="mes", columns="tipo", values="monto")
        .fillna(0)
        .reset_index()
    )
    resultado = []
    for r in tabla.itertuples(index=False):
        resultado.append(
            {
                "mes": r.mes,
                "ingresos": round(float(getattr(r, "ingreso", 0.0)), 2),
                "gastos": round(float(getattr(r, "gasto", 0.0)), 2),
            }
        )
    return resultado