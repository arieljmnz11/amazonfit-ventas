"""Lectura del archivo de ventas."""

from collections.abc import Iterator
from pathlib import Path

import pandas as pd

from amazonfit.config import COLUMNAS_REQUERIDAS, TIPOS_COLUMNAS


def cargar_ventas(ruta: Path) -> pd.DataFrame:
    """Lee el CSV de ventas con los tipos de dato correctos.

    Args:
        ruta: Ubicación del archivo CSV de ventas.

    Returns:
        DataFrame con una fila por venta registrada.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si al archivo le faltan columnas obligatorias.

    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo de ventas en {ruta}")

    ventas = pd.read_csv(ruta, dtype=TIPOS_COLUMNAS, parse_dates=["fecha"], encoding="utf-8")
    _validar_columnas(ventas)
    return ventas


def leer_en_bloques(ruta: Path, tamano_bloque: int = 50_000) -> Iterator[pd.DataFrame]:
    """Entrega el archivo de ventas por partes para no cargarlo entero en memoria.

    Es útil cuando el historial crezca a millones de filas.

    Args:
        ruta: Ubicación del archivo CSV de ventas.
        tamano_bloque: Número de filas por bloque.

    Yields:
        Un DataFrame con hasta ``tamano_bloque`` filas.

    """
    lector = pd.read_csv(
        ruta, dtype=TIPOS_COLUMNAS, parse_dates=["fecha"], encoding="utf-8", chunksize=tamano_bloque
    )
    with lector:
        for bloque in lector:
            yield bloque


def _validar_columnas(ventas: pd.DataFrame) -> None:
    """Comprueba que estén todas las columnas que usa el análisis."""
    faltantes = set(COLUMNAS_REQUERIDAS) - set(ventas.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas en el archivo de ventas: {sorted(faltantes)}")
