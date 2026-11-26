"""Métricas de ventas calculadas con operaciones vectorizadas de pandas."""

from collections.abc import Iterable

import numpy as np
import pandas as pd

from amazonfit.config import CATEGORIAS_CALZADO, DESCUENTO_EFECTIVO
from amazonfit.limpieza import limpiar_ventas


def agregar_ingreso(ventas: pd.DataFrame) -> pd.DataFrame:
    """Añade la columna ``ingreso`` con el descuento por pago en efectivo.

    El cálculo se hace sobre toda la columna a la vez, sin recorrer fila por fila.

    Args:
        ventas: Ventas limpias.

    Returns:
        Copia de las ventas con la columna ``ingreso`` en dólares.

    """
    # np.where aplica el descuento a todas las filas a la vez, sin un if por cada venta
    factor_pago = np.where(ventas["metodo_pago"] == "Efectivo", 1 - DESCUENTO_EFECTIVO, 1.0)
    return ventas.assign(ingreso=ventas["cantidad"] * ventas["precio_unitario"] * factor_pago)


def resumen_general(ventas: pd.DataFrame) -> dict[str, float]:
    """Calcula el número de ventas, las unidades y los ingresos totales."""
    return {
        "ventas": len(ventas),
        "unidades": int(ventas["cantidad"].sum()),
        "ingresos": round(float(ventas["ingreso"].sum()), 2),
    }


def ingresos_por_categoria(ventas: pd.DataFrame) -> pd.Series:
    """Suma los ingresos de cada categoría, de mayor a menor."""
    return ventas.groupby("categoria")["ingreso"].sum().round(2).sort_values(ascending=False)


def ingresos_por_mes(ventas: pd.DataFrame) -> pd.Series:
    """Suma los ingresos de cada mes en orden cronológico, con el mes como texto AAAA-MM.

    Agrupa por periodo mensual y convierte a texto solo las etiquetas del
    resultado, no las 200 000 fechas, porque esa conversión fila por fila es lenta.
    """
    # to_period agrupa por mes mucho más rápido que convertir cada fecha a texto con strftime    
    por_mes = ventas.groupby(ventas["fecha"].dt.to_period("M"))["ingreso"].sum().round(2).sort_index()
    por_mes.index = por_mes.index.astype(str)
    return por_mes


def productos_mas_vendidos(ventas: pd.DataFrame, cantidad: int = 10) -> pd.Series:
    """Devuelve los productos con más unidades vendidas.

    Args:
        ventas: Ventas limpias.
        cantidad: Cuántos productos incluir en el ranking.

    Returns:
        Unidades vendidas por producto, de mayor a menor.

    """
    return ventas.groupby("producto")["cantidad"].sum().nlargest(cantidad)


def tallas_mas_vendidas(ventas: pd.DataFrame, categoria: str, cantidad: int = 5) -> pd.Series:
    """Devuelve las tallas con más unidades vendidas dentro de una categoría de calzado.

    Raises:
        ValueError: Si la categoría no corresponde a zapatillas.

    """
    if categoria not in CATEGORIAS_CALZADO:
        raise ValueError(f"{categoria} no es una categoría de zapatillas")
    calzado = ventas[ventas["categoria"] == categoria]
    return calzado.groupby("talla")["cantidad"].sum().nlargest(cantidad)


def marcas_de_zapatillas(ventas: pd.DataFrame) -> pd.DataFrame:
    """Resume las unidades de zapatillas por marca y el porcentaje vendido de segunda mano."""
    zapatillas = ventas[ventas["categoria"].isin(CATEGORIAS_CALZADO)]
    unidades_segunda = zapatillas["cantidad"].where(zapatillas["condicion"] == "Segunda mano", 0)
    resumen = (
        zapatillas.assign(unidades_segunda=unidades_segunda)
        .groupby("marca", observed=True)[["cantidad", "unidades_segunda"]]
        .sum()
        .rename(columns={"cantidad": "unidades"})
    )
    resumen["porcentaje_segunda"] = (resumen["unidades_segunda"] / resumen["unidades"] * 100).round(1)
    return resumen.sort_values("unidades", ascending=False)[["unidades", "porcentaje_segunda"]]


def ingresos_por_mes_en_bloques(bloques: Iterable[pd.DataFrame]) -> pd.Series:
    """Calcula los ingresos por mes leyendo el archivo por partes.

    Recibe un generador como ``leer_en_bloques`` y solo guarda en memoria los
    subtotales de cada bloque, no todas las filas.

    Nota: los duplicados se eliminan dentro de cada bloque. Si un duplicado cae
    en otro bloque, no se detecta.
    """
    subtotales = (ingresos_por_mes(agregar_ingreso(limpiar_ventas(bloque)[0])) for bloque in bloques)
    return pd.concat(subtotales).groupby(level=0).sum().round(2)
