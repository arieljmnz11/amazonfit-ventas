"""Genera datos ficticios de ventas de AmazonFit Store, tienda de running y trail en Tena.

Los datos son simulados para la actividad académica. Incluyen a propósito un
pequeño porcentaje de filas con problemas reales de captura, como ventas
duplicadas, precios vacíos, cantidades negativas y categorías mal escritas,
para que la etapa de limpieza tenga sentido.

Uso:
    python scripts/generar_datos.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 2026
NUMERO_VENTAS = 200_000
FECHA_INICIO = "2024-01-01"
FECHA_FIN = "2026-10-31"
RUTA_SALIDA = Path(__file__).resolve().parents[1] / "datos" / "ventas_amazonfit.csv"

TALLAS_ZAPATILLA = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
PESOS_TALLA_ZAPATILLA = [0.03, 0.06, 0.10, 0.14, 0.17, 0.17, 0.14, 0.10, 0.06, 0.03]
TALLAS_ROPA = ["S", "M", "L", "XL"]
PESOS_TALLA_ROPA = [0.25, 0.40, 0.25, 0.10]

# Cada producto: categoria, producto, marca, precio nuevo, precio de segunda
# (None si solo se vende nuevo), popularidad relativa y tipo de talla.
CATALOGO = [
    # Zapatillas de asfalto: lo que más se mueve en Tena por el calor y las rutas cortas.
    ("Zapatillas de asfalto", "Adizero Adios Pro 3", "Adidas", 180.0, 75.0, 5, "calzado"),
    ("Zapatillas de asfalto", "Adizero Boston 12", "Adidas", 120.0, 55.0, 7, "calzado"),
    ("Zapatillas de asfalto", "Adizero SL", "Adidas", 85.0, 40.0, 8, "calzado"),
    ("Zapatillas de asfalto", "Clifton 9", "Hoka", 115.0, 50.0, 8, "calzado"),
    ("Zapatillas de asfalto", "Rincon 3", "Hoka", 95.0, 45.0, 6, "calzado"),
    ("Zapatillas de asfalto", "Pegasus 40", "Nike", 100.0, 45.0, 6, "calzado"),
    ("Zapatillas de asfalto", "Novablast 4", "Asics", 110.0, 50.0, 5, "calzado"),
    ("Zapatillas de asfalto", "Running básica", "Sin marca", 25.0, None, 12, "calzado"),
    # Zapatillas de trail: rutas cortas y con poco desnivel.
    ("Zapatillas de trail", "Speedgoat 5", "Hoka", 120.0, 55.0, 6, "calzado"),
    ("Zapatillas de trail", "Challenger ATR 7", "Hoka", 110.0, 50.0, 5, "calzado"),
    ("Zapatillas de trail", "Speedcross 6", "Salomon", 115.0, 50.0, 4, "calzado"),
    ("Zapatillas de trail", "Terrex Agravic Flow", "Adidas", 90.0, 40.0, 4, "calzado"),
    ("Zapatillas de trail", "Pegasus Trail 4", "Nike", 95.0, 45.0, 3, "calzado"),
    ("Zapatillas de trail", "Gel-Trabuco 11", "Asics", 85.0, 40.0, 3, "calzado"),
    ("Zapatillas de trail", "Trail básica", "Sin marca", 28.0, None, 9, "calzado"),
    # Indumentaria
    ("Indumentaria", "Camiseta técnica manga corta", "Sin marca", 9.0, None, 14, "ropa"),
    ("Indumentaria", "Camiseta técnica sin mangas", "Sin marca", 8.0, None, 9, "ropa"),
    ("Indumentaria", "Mangas compresivas", "Sin marca", 7.0, None, 4, "ropa"),
    ("Indumentaria", "Buff multiuso", "Sin marca", 5.0, None, 7, "unica"),
    ("Shorts traileros", "Short trailero con bolsillos", "Sin marca", 15.0, None, 9, "ropa"),
    ("Shorts traileros", "Short running liviano", "Sin marca", 12.0, None, 8, "ropa"),
    ("Shorts traileros", "Short con licra interna", "Sin marca", 18.0, None, 5, "ropa"),
    # Medias
    ("Medias de running", "Media tobillera", "Sin marca", 3.0, None, 16, "unica"),
    ("Medias de running", "Media compresiva", "Sin marca", 6.0, None, 6, "unica"),
    ("Medias de trail", "Media trail caña media", "Sin marca", 5.0, None, 8, "unica"),
    ("Medias de trail", "Media trail lana merino", "Sin marca", 9.0, None, 3, "unica"),
    # Gorras
    ("Gorras y viseras", "Gorra running ventilada", "Sin marca", 8.0, None, 9, "unica"),
    ("Gorras y viseras", "Visera running", "Sin marca", 6.0, None, 6, "unica"),
    ("Gorras y viseras", "Gorra con cubrenuca", "Sin marca", 11.0, None, 3, "unica"),
    # Nutrición
    ("Geles y electrolitos", "Gel energético", "Sin marca", 2.5, None, 18, "unica"),
    ("Geles y electrolitos", "Gel con cafeína", "Sin marca", 3.0, None, 8, "unica"),
    ("Geles y electrolitos", "Sobre de electrolitos", "Sin marca", 1.5, None, 14, "unica"),
    ("Barritas energéticas", "Barrita de avena y miel", "Sin marca", 1.5, None, 14, "unica"),
    ("Barritas energéticas", "Barrita de proteína", "Sin marca", 2.5, None, 7, "unica"),
    # Hidratación
    ("Chalecos de hidratación", "Chaleco 5 litros", "Sin marca", 30.0, None, 4, "unica"),
    ("Chalecos de hidratación", "Chaleco 12 litros", "Sin marca", 45.0, None, 1, "unica"),
    ("Flasks", "Flask blando 500 ml", "Sin marca", 9.0, None, 7, "unica"),
    ("Flasks", "Flask blando 250 ml", "Sin marca", 7.0, None, 4, "unica"),
    ("Canguros y cinturones", "Canguro running", "Sin marca", 10.0, None, 8, "unica"),
    ("Canguros y cinturones", "Cinturón con porta flask", "Sin marca", 15.0, None, 4, "unica"),
    # Otros accesorios
    ("Frontales", "Frontal 300 lúmenes", "Sin marca", 12.0, None, 4, "unica"),
    ("Frontales", "Frontal recargable 500 lúmenes", "Sin marca", 25.0, None, 2, "unica"),
    ("Bastones", "Bastones plegables de aluminio", "Sin marca", 35.0, None, 1, "unica"),
    ("Accesorios para celular", "Brazalete porta celular", "Sin marca", 7.0, None, 8, "unica"),
    ("Accesorios para celular", "Funda impermeable", "Sin marca", 5.0, None, 5, "unica"),
    ("Accesorios para celular", "Cinturón porta celular", "Sin marca", 9.0, None, 4, "unica"),
]

COLUMNAS_CATALOGO = [
    "categoria", "producto", "marca", "precio_nuevo", "precio_segunda", "popularidad", "tipo_talla",
]


def _factor_estacional(fechas: pd.DatetimeIndex) -> np.ndarray:
    """Calcula un peso por día que imita el boom del running y las temporadas altas.

    Las ventas crecen poco a poco desde 2024 y suben en vacaciones de julio y agosto
    y en noviembre y diciembre.
    """
    progreso = np.linspace(0.0, 1.0, len(fechas))
    tendencia = 1.0 + 0.8 * progreso
    temporada = np.where(fechas.month.isin([7, 8]), 1.25, 1.0)
    temporada = np.where(fechas.month.isin([11, 12]), 1.35, temporada)
    fin_de_semana = np.where(fechas.dayofweek >= 5, 1.3, 1.0)
    return tendencia * temporada * fin_de_semana


def generar_ventas(numero_ventas: int, semilla: int) -> pd.DataFrame:
    """Crea un DataFrame de ventas simuladas con algunas filas sucias."""
    generador = np.random.default_rng(semilla)
    catalogo = pd.DataFrame(CATALOGO, columns=COLUMNAS_CATALOGO)

    dias = pd.date_range(FECHA_INICIO, FECHA_FIN, freq="D")
    pesos_dia = _factor_estacional(dias)
    fechas = generador.choice(dias, size=numero_ventas, p=pesos_dia / pesos_dia.sum())

    pesos_producto = catalogo["popularidad"] / catalogo["popularidad"].sum()
    indices = generador.choice(len(catalogo), size=numero_ventas, p=pesos_producto)
    ventas = catalogo.iloc[indices].reset_index(drop=True)

    tiene_segunda = ventas["precio_segunda"].notna().to_numpy()
    es_segunda = tiene_segunda & (generador.random(numero_ventas) < 0.62)
    ventas["condicion"] = np.where(es_segunda, "Segunda mano", "Nueva")
    precio_base = np.where(es_segunda, ventas["precio_segunda"], ventas["precio_nuevo"])
    variacion = generador.uniform(0.9, 1.1, numero_ventas)
    ventas["precio_unitario"] = np.round(precio_base * variacion * 2) / 2

    talla = np.full(numero_ventas, "Única", dtype=object)
    es_calzado = (ventas["tipo_talla"] == "calzado").to_numpy()
    es_ropa = (ventas["tipo_talla"] == "ropa").to_numpy()
    talla[es_calzado] = generador.choice(TALLAS_ZAPATILLA, es_calzado.sum(), p=PESOS_TALLA_ZAPATILLA).astype(str)
    talla[es_ropa] = generador.choice(TALLAS_ROPA, es_ropa.sum(), p=PESOS_TALLA_ROPA)
    ventas["talla"] = talla

    es_consumible = ventas["categoria"].isin(["Geles y electrolitos", "Barritas energéticas"]).to_numpy()
    es_media = ventas["categoria"].str.startswith("Medias").to_numpy()
    cantidad = np.ones(numero_ventas, dtype=int)
    cantidad[es_consumible] = generador.integers(1, 7, es_consumible.sum())
    cantidad[es_media] = generador.integers(1, 4, es_media.sum())
    ventas["cantidad"] = cantidad

    ventas["metodo_pago"] = generador.choice(
        ["Efectivo", "Transferencia", "Tarjeta"], numero_ventas, p=[0.5, 0.4, 0.1]
    )
    ventas["canal"] = generador.choice(["Tienda", "WhatsApp", "Instagram"], numero_ventas, p=[0.6, 0.3, 0.1])
    ventas["fecha"] = pd.to_datetime(fechas).strftime("%Y-%m-%d")

    ventas = ventas.sort_values("fecha", kind="stable").reset_index(drop=True)
    ventas.insert(0, "id_venta", [f"V{numero:06d}" for numero in range(1, numero_ventas + 1)])
    columnas = [
        "id_venta", "fecha", "categoria", "producto", "marca", "talla",
        "condicion", "cantidad", "precio_unitario", "metodo_pago", "canal",
    ]
    ventas = ventas[columnas]
    return _ensuciar(ventas, generador)


def _ensuciar(ventas: pd.DataFrame, generador: np.random.Generator) -> pd.DataFrame:
    """Introduce errores típicos de captura en una fracción pequeña de filas."""
    ventas = ventas.copy()
    ventas["precio_unitario"] = ventas["precio_unitario"].map(lambda precio: f"{precio:.2f}")
    total = len(ventas)

    mal_escritas = generador.choice(total, int(total * 0.004), replace=False)
    variantes = [lambda texto: texto.upper() + " ", lambda texto: " " + texto.lower()]
    for posicion, fila in enumerate(mal_escritas):
        ventas.at[fila, "categoria"] = variantes[posicion % 2](ventas.at[fila, "categoria"])

    sin_precio = generador.choice(total, int(total * 0.003), replace=False)
    ventas.loc[sin_precio, "precio_unitario"] = ""

    negativas = generador.choice(total, int(total * 0.002), replace=False)
    ventas.loc[negativas, "cantidad"] = -ventas.loc[negativas, "cantidad"]

    duplicadas = ventas.sample(n=int(total * 0.006), random_state=SEMILLA)
    ventas = pd.concat([ventas, duplicadas]).sort_values(["fecha", "id_venta"], kind="stable")
    return ventas.reset_index(drop=True)


def main() -> None:
    """Genera el archivo CSV de ventas en la carpeta datos."""
    ventas = generar_ventas(NUMERO_VENTAS, SEMILLA)
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    ventas.to_csv(RUTA_SALIDA, index=False, encoding="utf-8")
    print(f"Archivo generado en {RUTA_SALIDA} con {len(ventas):,} filas")


if __name__ == "__main__":
    main()
