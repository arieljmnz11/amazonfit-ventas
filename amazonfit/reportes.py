"""Construcción del reporte de texto con los resultados."""

import pandas as pd

from amazonfit.limpieza import ResumenLimpieza


def formatear_dolares(valor: float) -> str:
    """Convierte un número en texto con formato de dólares, por ejemplo 1234.5 a $1,234.50."""
    return f"${valor:,.2f}"


def _seccion(titulo: str, lineas: list[str]) -> str:
    """Une un título y sus líneas en un bloque del reporte."""
    return "\n".join([f"\n== {titulo} ==", *lineas])


def generar_reporte(
    limpieza: ResumenLimpieza,
    resumen: dict[str, float],
    por_categoria: pd.Series,
    por_mes: pd.Series,
    top_productos: pd.Series,
    tallas: dict[str, pd.Series],
    marcas: pd.DataFrame,
) -> str:
    """Arma el reporte completo de ventas de AmazonFit Store como texto.

    Returns:
        Texto listo para imprimir o guardar en un archivo.

    """
    secciones = [
        _seccion("Limpieza de datos", [
            f"Filas leídas: {limpieza.filas_iniciales:,}",
            f"Duplicadas eliminadas: {limpieza.duplicadas:,}",
            f"Sin precio eliminadas: {limpieza.sin_precio:,}",
            f"Con cantidad no válida eliminadas: {limpieza.cantidad_invalida:,}",
            f"Filas analizadas: {limpieza.filas_finales:,}",
        ]),
        _seccion("Resumen general", [
            f"Ventas: {resumen['ventas']:,}",
            f"Unidades: {resumen['unidades']:,}",
            f"Ingresos: {formatear_dolares(resumen['ingresos'])}",
        ]),
        _seccion("Ingresos por categoría", [
            f"{categoria}: {formatear_dolares(valor)}" for categoria, valor in por_categoria.items()
        ]),
        _seccion("Ingresos por mes", [f"{mes}: {formatear_dolares(valor)}" for mes, valor in por_mes.items()]),
        _seccion("Productos más vendidos", [
            f"{posicion}. {producto}: {unidades:,} unidades"
            for posicion, (producto, unidades) in enumerate(top_productos.items(), start=1)
        ]),
        *[
            _seccion(f"Tallas más vendidas en {categoria}", [
                f"Talla {talla}: {unidades:,} pares" for talla, unidades in serie.items()
            ])
            for categoria, serie in tallas.items()
        ],
        _seccion("Zapatillas por marca", [
            f"{fila.Index}: {int(fila.unidades):,} pares, {fila.porcentaje_segunda}% de segunda mano"
            for fila in marcas.itertuples()
        ]),
    ]
    return "\n".join(secciones)
