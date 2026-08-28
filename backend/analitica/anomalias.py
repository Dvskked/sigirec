"""Detección de anomalías en gastos mediante Z-Score.

Compara cada movimiento contra la media y desviación del gasto de su misma
categoría. Si |z| > umbral, el movimiento se considera una anomalía.
"""

from .agregaciones import _dataframe_movimientos

UMBRAL_Z = 2.0


def detectar_anomalias(movimientos, umbral_z=UMBRAL_Z):
    """Devuelve la lista de movimientos anómalos con su z-score."""
    df = _dataframe_movimientos(movimientos)
    if df.empty:
        return []

    gastos = df[df["tipo"] == "gasto"].copy()
    if gastos.empty:
        return []

    stats = (
        gastos.groupby("id_categoria")["monto"]
        .agg(["mean", "std"])
        .reset_index()
    )
    # Evita std = 0 (categorías con un único valor o monto constante).
    stats["std"] = stats["std"].fillna(0)

    gastos = gastos.merge(stats, on="id_categoria", how="left")
    gastos["z_score"] = (gastos["monto"] - gastos["mean"]) / gastos["std"].replace(0, 1)

    anomalias = gastos[gastos["z_score"].abs() > umbral_z]

    filas = []
    for r in anomalias.sort_values("z_score", ascending=False).itertuples(index=False):
        filas.append(
            {
                "id_movimiento": int(r.id_movimiento),
                "id_categoria": int(r.id_categoria),
                "categoria": r.categoria,
                "tipo": "gasto",
                "monto": round(float(r.monto), 2),
                "fecha": r.fecha.strftime("%Y-%m-%d"),
                "descripcion": r.descripcion or "",
                "z_score": round(float(r.z_score), 2),
                "promedio_categoria": round(float(r.mean), 2),
                "motivo": "Gasto que se desvía notablemente del patrón histórico "
                          "de su categoría (|Z| > 2).",
            }
        )
    return filas