"""Compara la versión original y la versión optimizada del análisis.

Hace dos cosas:
1. Verifica que, con los mismos datos limpios, ambas versiones den los mismos totales.
2. Mide el tiempo de cada versión con 200 000 y con 1 000 000 de filas.

Uso:
    python scripts/comparar_rendimiento.py
"""

import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts"))

from generar_datos import SEMILLA, generar_ventas  # noqa: E402

from amazonfit.carga import cargar_ventas  # noqa: E402
from amazonfit.limpieza import limpiar_ventas  # noqa: E402
from amazonfit.metricas import agregar_ingreso, resumen_general  # noqa: E402

SCRIPT_ORIGINAL = RAIZ / "original" / "analisis_ventas_original.py"
REPETICIONES = 3


def _preparar_carpeta(ventas_csv: Path) -> Path:
    """Crea una carpeta temporal con la ruta relativa que espera el script original."""
    carpeta = Path(tempfile.mkdtemp())
    (carpeta / "datos").mkdir()
    shutil.copy(ventas_csv, carpeta / "datos" / "ventas_amazonfit.csv")
    return carpeta


def _medir(comando: list[str], carpeta: Path) -> tuple[float, str]:
    """Ejecuta un comando varias veces y devuelve la mediana del tiempo y la última salida."""
    tiempos = []
    salida = ""
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        resultado = subprocess.run(comando, cwd=carpeta, capture_output=True, text=True, check=True)
        tiempos.append(time.perf_counter() - inicio)
        salida = resultado.stdout
    return statistics.median(tiempos), salida


def _leer_total(salida: str, etiqueta: str) -> float:
    """Extrae un número de la salida del script original, por ejemplo la línea INGRESOS."""
    linea = next(linea for linea in salida.splitlines() if linea.startswith(etiqueta))
    return float(linea.split(":")[1])


def verificar_equivalencia(ventas_csv: Path) -> None:
    """Corre el script original sobre datos ya limpios y compara sus totales con la versión nueva."""
    ventas, _ = limpiar_ventas(cargar_ventas(ventas_csv))
    carpeta = Path(tempfile.mkdtemp())
    (carpeta / "datos").mkdir()
    ventas.to_csv(carpeta / "datos" / "ventas_amazonfit.csv", index=False, date_format="%Y-%m-%d")

    _, salida = _medir([sys.executable, str(SCRIPT_ORIGINAL)], carpeta)
    nuevo = resumen_general(agregar_ingreso(ventas))
    original = {
        "ventas": _leer_total(salida, "TOTAL VENTAS"),
        "unidades": _leer_total(salida, "UNIDADES"),
        "ingresos": _leer_total(salida, "INGRESOS"),
    }
    print("\nEquivalencia con datos limpios")
    for clave, valor in nuevo.items():
        # Se acepta hasta 2 centavos de diferencia porque sumar 200 000 decimales en
        # distinto orden produce pequeñas diferencias de redondeo.
        coincide = abs(valor - original[clave]) <= 0.02
        print(f"  {clave}: original {original[clave]:,.2f} | nueva {valor:,.2f} | coincide {coincide}")
    shutil.rmtree(carpeta)


def comparar_tiempos(ventas_csv: Path, etiqueta: str) -> None:
    """Mide ambas versiones sobre el mismo archivo."""
    carpeta = _preparar_carpeta(ventas_csv)
    tiempo_original, _ = _medir([sys.executable, str(SCRIPT_ORIGINAL)], carpeta)
    tiempo_nuevo, _ = _medir(
        [sys.executable, str(RAIZ / "main.py"), "--datos", str(carpeta / "datos" / "ventas_amazonfit.csv")],
        RAIZ,
    )
    print(
        f"{etiqueta}: original {tiempo_original:.2f} s | optimizada {tiempo_nuevo:.2f} s | "
        f"{tiempo_original / tiempo_nuevo:.1f} veces más rápida"
    )
    shutil.rmtree(carpeta)


def main() -> None:
    """Ejecuta la verificación y las mediciones."""
    datos_reales = RAIZ / "datos" / "ventas_amazonfit.csv"
    verificar_equivalencia(datos_reales)

    print(f"\nTiempos, mediana de {REPETICIONES} ejecuciones")
    comparar_tiempos(datos_reales, "200 000 filas")

    with tempfile.TemporaryDirectory() as carpeta:
        archivo_grande = Path(carpeta) / "ventas_grande.csv"
        generar_ventas(1_000_000, SEMILLA).to_csv(archivo_grande, index=False)
        comparar_tiempos(archivo_grande, "1 000 000 filas")


if __name__ == "__main__":
    main()
