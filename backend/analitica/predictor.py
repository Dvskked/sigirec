"""Predicción del gasto del próximo mes con regresión lineal.

El modelo usa la tendencia histórica de gasto acumulado por mes
(LinearRegression de scikit-learn). Cuando hay pocos datos para entrenar,
se devuelve un valor de respaldo basado en el promedio histórico.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression

from .agregaciones import _dataframe_movimientos

# Con este mínimo de meses la regresión es estadísticamente razonable.
MIN_MESES_MODELO = 3


def predecir_gasto_proximo_mes(movimientos):
    """Devuelve un dict con la predicción y desglose por categoría."""
    df = _dataframe_movimientos(movimientos)
    respuesta = {
        "id_usuario": None,
        "prediccion_proximo_mes": None,
        "metodo": "regresion_lineal",
        "confianza": "media",
        "detalle_por_categoria": {},
        "meses_considerados": 0,
        "mensaje": "",
    }

    if df.empty:
        respuesta.update({"metodo": "sin_datos", "confianza": "baja",
                          "mensaje": "No hay movimientos registrados."})
        return respuesta

    gastos = df[df["tipo"] == "gasto"]
    if gastos.empty:
        respuesta.update({"metodo": "sin_datos", "confianza": "baja",
                          "mensaje": "No hay gastos registrados."})
        return respuesta

    # --- Resumen mensual de gasto total ---
    resumen_mensual = (
        gastos.groupby("mes")["monto"].sum().reset_index().sort_values("mes")
    )
    resumen_mensual["n_mes"] = range(len(resumen_mensual))

    # --- Opción 1: regresión lineal ---
    if len(resumen_mensual) >= MIN_MESES_MODELO:
        X = resumen_mensual[["n_mes"]].to_numpy()
        y = resumen_mensual["monto"].to_numpy()
        modelo = LinearRegression()
        modelo.fit(X, y)
        siguiente_n = [[len(resumen_mensual)]]
        prediccion = float(modelo.predict(siguiente_n)[0])
        confianza = _calcular_confianza(resumen_mensual)
        metodo = "regresion_lineal"
    else:
        # Opción 2 (respaldo): promedio histórico.
        prediccion = float(resumen_mensual["monto"].mean())
        confianza = "baja"
        metodo = "promedio_historico"

    prediccion = max(prediccion, 0.0)

    # --- Desglose por categoría (regresión simple por categoría) ---
    detalle = {}
    for categoria, grupo in gastos.groupby("categoria"):
        serie = (
            grupo.groupby("mes")["monto"]
            .sum()
            .reset_index()
            .sort_values("mes")
        )
        serie["n_mes"] = range(len(serie))
        if len(serie) >= 2:
            modelo_cat = LinearRegression()
            modelo_cat.fit(serie[["n_mes"]].to_numpy(), serie["monto"].to_numpy())
            valor = float(modelo_cat.predict([[len(serie)]])[0])
        else:
            valor = float(serie["monto"].mean())
        detalle[categoria] = round(max(valor, 0.0), 2)

    respuesta.update(
        {
            "prediccion_proximo_mes": round(prediccion, 2),
            "metodo": metodo,
            "confianza": confianza,
            "detalle_por_categoria": dict(sorted(detalle.items(), key=lambda i: -i[1])),
            "meses_considerados": int(len(resumen_mensual)),
            "mensaje": "Predicción estimada a partir de la tendencia mensual.",
            "ultimo_mes": str(resumen_mensual["mes"].iloc[-1]) if len(resumen_mensual) else None,
        }
    )
    return respuesta


def _calcular_confianza(resumen_mensual):
    """Confianza simple según dispersión relativa de la serie."""
    if len(resumen_mensual) < MIN_MESES_MODELO:
        return "baja"
    desv = resumen_mensual["monto"].std()
    media = resumen_mensual["monto"].mean()
    if media <= 0:
        return "media"
    cv = desv / media
    if cv < 0.15:
        return "alta"
    if cv < 0.4:
        return "media"
    return "baja"