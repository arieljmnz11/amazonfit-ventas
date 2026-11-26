"""Mide por separado cada técnica de optimización aplicada.

Compara, sobre los mismos datos limpios, la forma en que lo hacía el código
original contra la forma optimizada.

Uso:
    python scripts/micro_comparaciones.py
"""

import sys
import time
import tracemalloc
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from amazonfit.carga import cargar_ventas  # noqa: E402
from amazonfit.config import RUTA_DATOS  # noqa: E402
from amazonfit.limpieza import limpiar_ventas  # noqa: E402
from amazonfit.metricas import agregar_ingreso, ingresos_por_mes, productos_mas_vendidos  # noqa: E402


def cronometrar(funcion) -> float:
    """Devuelve los segundos que tarda una función, tomando la mejor de tres ejecuciones."""
    tiempos = []
    for _ in range(3):
        inicio = time.perf_counter()
        funcion()
        tiempos.append(time.perf_counter() - inicio)
    return min(tiempos)


def imprimir(nombre: str, lento: float, rapido: float) -> None:
    """Muestra una comparación de tiempos en una línea."""
    print(f"{nombre}: original {lento:.4f} s | optimizada {rapido:.4f} s | {lento / rapido:,.0f} veces")


def main() -> None:
    """Ejecuta las comparaciones técnica por técnica."""
    ventas = agregar_ingreso(limpiar_ventas(cargar_ventas(RUTA_DATOS))[0])
    filas = ventas[["fecha", "producto", "cantidad", "ingreso"]].astype(str).values.tolist()
    nombres = ventas["producto"].tolist()

    def unicos_con_lista():
        vistos = []
        for nombre in nombres:
            if nombre not in vistos:
                vistos.append(nombre)

    imprimir("Productos únicos, lista contra set", cronometrar(unicos_con_lista), cronometrar(lambda: set(nombres)))

    def unidades_con_bucles():
        resultado = []
        for producto in set(nombres):
            total = 0
            for fila in filas:
                if fila[1] == producto:
                    total += int(fila[2])
            resultado.append([producto, total])
        return resultado

    imprimir(
        "Unidades por producto, bucles anidados contra groupby",
        cronometrar(unidades_con_bucles),
        cronometrar(lambda: productos_mas_vendidos(ventas, 10)),
    )

    def ingresos_mes_con_bucles():
        meses = sorted({fila[0][:7] for fila in filas})
        return [sum(float(fila[3]) for fila in filas if fila[0][:7] == mes) for mes in meses]

    imprimir(
        "Ingresos por mes, bucles anidados contra groupby",
        cronometrar(ingresos_mes_con_bucles),
        cronometrar(lambda: ingresos_por_mes(ventas)),
    )

    ranking = [[nombre, total] for nombre, total in unidades_con_bucles()]

    def burbuja():
        copia = [fila[:] for fila in ranking] * 20
        for _ in range(len(copia)):
            for j in range(len(copia) - 1):
                if copia[j][1] < copia[j + 1][1]:
                    copia[j], copia[j + 1] = copia[j + 1], copia[j]

    imprimir(
        f"Ordenar ranking de {len(ranking) * 20} elementos, burbuja contra sorted",
        cronometrar(burbuja),
        cronometrar(lambda: sorted(ranking * 20, key=lambda fila: fila[1], reverse=True)),
    )

    precios = ventas["ingreso"].tolist()
    tracemalloc.start()
    sum([precio for precio in precios])
    _, pico_lista = tracemalloc.get_traced_memory()
    tracemalloc.reset_peak()
    sum(precio for precio in precios)
    _, pico_generador = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(
        f"Memoria al sumar ingresos: lista {pico_lista / 1024:,.0f} KB | "
        f"generador {pico_generador / 1024:,.1f} KB"
    )


if __name__ == "__main__":
    main()
