"""Pruebas unitarias del módulo de limpieza."""

import pandas as pd

from amazonfit.limpieza import limpiar_ventas, normalizar_categorias


def test_normalizar_categorias_unifica_mayusculas_y_espacios():
    categorias = pd.Series([" ZAPATILLAS DE TRAIL ", "zapatillas de trail", "Zapatillas de trail"])
    assert normalizar_categorias(categorias).nunique() == 1


def test_limpiar_ventas_elimina_cada_tipo_de_error(ventas_crudas):
    limpias, resumen = limpiar_ventas(ventas_crudas)

    assert resumen.duplicadas == 1
    assert resumen.sin_precio == 1
    assert resumen.cantidad_invalida == 1
    assert resumen.filas_finales == 3
    assert len(limpias) == 3


def test_limpiar_ventas_no_modifica_el_dataframe_original(ventas_crudas):
    copia = ventas_crudas.copy()
    limpiar_ventas(ventas_crudas)
    pd.testing.assert_frame_equal(ventas_crudas, copia)
