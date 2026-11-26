"""Limpieza de las ventas antes de calcular métricas."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ResumenLimpieza:
    """Cuántas filas se descartaron y por qué."""

    filas_iniciales: int
    duplicadas: int
    sin_precio: int
    cantidad_invalida: int
    filas_finales: int


def normalizar_categorias(categorias: pd.Series) -> pd.Series:
    """Unifica la escritura de las categorías.

    Quita espacios sobrantes y deja solo la primera letra en mayúscula, de modo
    que " ZAPATILLAS DE TRAIL " y "zapatillas de trail" cuenten como la misma.

    Args:
        categorias: Columna de categorías tal como viene del archivo.

    Returns:
        Columna con las categorías escritas de forma uniforme.

    """
    return categorias.str.strip().str.capitalize()


def limpiar_ventas(ventas: pd.DataFrame) -> tuple[pd.DataFrame, ResumenLimpieza]:
    """Elimina duplicados, precios vacíos y cantidades no válidas.

    Args:
        ventas: Ventas tal como las devuelve ``cargar_ventas``.

    Returns:
        Una tupla con las ventas limpias y el resumen de lo descartado.

    """
    filas_iniciales = len(ventas)

    ventas = ventas.drop_duplicates()
    duplicadas = filas_iniciales - len(ventas)

    sin_precio = int(ventas["precio_unitario"].isna().sum())
    ventas = ventas.dropna(subset=["precio_unitario"])

    cantidad_valida = ventas["cantidad"] > 0
    cantidad_invalida = int((~cantidad_valida).sum())
    ventas = ventas[cantidad_valida].copy()

    ventas["categoria"] = normalizar_categorias(ventas["categoria"])
    ventas["cantidad"] = ventas["cantidad"].astype("int64")

    resumen = ResumenLimpieza(
        filas_iniciales=filas_iniciales,
        duplicadas=duplicadas,
        sin_precio=sin_precio,
        cantidad_invalida=cantidad_invalida,
        filas_finales=len(ventas),
    )
    return ventas, resumen
