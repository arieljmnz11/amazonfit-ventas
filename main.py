"""Punto de entrada: genera el reporte de ventas de AmazonFit Store.

Uso:
    python main.py
    python main.py --datos ruta/a/otro_archivo.csv
"""

import argparse
import logging
import time
from pathlib import Path

from amazonfit.carga import cargar_ventas
from amazonfit.config import CATEGORIAS_CALZADO, RUTA_DATOS
from amazonfit.limpieza import limpiar_ventas
from amazonfit.metricas import (
    agregar_ingreso,
    ingresos_por_categoria,
    ingresos_por_mes,
    marcas_de_zapatillas,
    productos_mas_vendidos,
    resumen_general,
    tallas_mas_vendidas,
)
from amazonfit.reportes import generar_reporte

logger = logging.getLogger("amazonfit")


def analizar(ruta_datos: Path) -> str:
    """Ejecuta todo el análisis y devuelve el reporte como texto."""
    ventas, resumen_limpieza = limpiar_ventas(cargar_ventas(ruta_datos))
    logger.info("Filas analizadas después de limpiar: %s", resumen_limpieza.filas_finales)
    ventas = agregar_ingreso(ventas)

    return generar_reporte(
        limpieza=resumen_limpieza,
        resumen=resumen_general(ventas),
        por_categoria=ingresos_por_categoria(ventas),
        por_mes=ingresos_por_mes(ventas),
        top_productos=productos_mas_vendidos(ventas),
        tallas={categoria: tallas_mas_vendidas(ventas, categoria) for categoria in sorted(CATEGORIAS_CALZADO)},
        marcas=marcas_de_zapatillas(ventas),
    )


def main() -> None:
    """Lee los argumentos, corre el análisis e imprime el reporte."""
    parser = argparse.ArgumentParser(description="Reporte de ventas de AmazonFit Store")
    parser.add_argument("--datos", type=Path, default=RUTA_DATOS, help="Ruta del CSV de ventas")
    parser.add_argument("--detalle", action="store_true", help="Muestra mensajes de depuración")
    argumentos = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if argumentos.detalle else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    inicio = time.perf_counter()
    print(analizar(argumentos.datos))
    logger.info("Análisis completado en %.2f segundos", time.perf_counter() - inicio)


if __name__ == "__main__":
    main()
