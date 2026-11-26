"""Prueba de integración: el flujo completo desde un CSV hasta el reporte."""

import pytest

from amazonfit.carga import cargar_ventas, leer_en_bloques
from amazonfit.limpieza import limpiar_ventas
from amazonfit.metricas import agregar_ingreso, ingresos_por_mes, ingresos_por_mes_en_bloques
from main import analizar


@pytest.fixture
def archivo_csv(ventas_crudas, tmp_path):
    """Guarda las ventas de ejemplo en un CSV temporal."""
    ruta = tmp_path / "ventas.csv"
    ventas_crudas.to_csv(ruta, index=False, date_format="%Y-%m-%d")
    return ruta


def test_reporte_completo_desde_csv(archivo_csv):
    reporte = analizar(archivo_csv)
    assert "Filas analizadas: 3" in reporte
    assert "Ingresos: $182.25" in reporte


def test_lectura_por_bloques_da_el_mismo_resultado(archivo_csv):
    completo = ingresos_por_mes(agregar_ingreso(limpiar_ventas(cargar_ventas(archivo_csv))[0]))
    # Bloques de 3 filas, para que los duplicados V2 queden en el mismo bloque.
    por_bloques = ingresos_por_mes_en_bloques(leer_en_bloques(archivo_csv, tamano_bloque=3))
    assert por_bloques.to_dict() == pytest.approx(completo.to_dict())


def test_archivo_inexistente_lanza_error_claro(tmp_path):
    with pytest.raises(FileNotFoundError, match="No se encontró"):
        cargar_ventas(tmp_path / "no_existe.csv")
