"""Pruebas unitarias de las métricas de ventas."""

import pytest

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


@pytest.fixture
def ventas(ventas_crudas):
    """Ventas de ejemplo ya limpias y con la columna de ingreso."""
    return agregar_ingreso(limpiar_ventas(ventas_crudas)[0])


def test_descuento_en_efectivo_es_de_cinco_por_ciento(ventas):
    speedgoat_efectivo = ventas[ventas["id_venta"] == "V1"]
    assert speedgoat_efectivo["ingreso"].iloc[0] == pytest.approx(55.0 * 0.95)


def test_resumen_general(ventas):
    assert resumen_general(ventas) == {"ventas": 3, "unidades": 6, "ingresos": 182.25}


def test_ingresos_por_categoria_ordena_de_mayor_a_menor(ventas):
    resultado = ingresos_por_categoria(ventas)
    assert list(resultado.index) == ["Zapatillas de trail", "Geles y electrolitos"]
    assert resultado.is_monotonic_decreasing


def test_ingresos_por_mes_usa_formato_anio_mes(ventas):
    resultado = ingresos_por_mes(ventas)
    assert list(resultado.index) == ["2025-07", "2025-08"]
    assert resultado.sum() == pytest.approx(182.25)


def test_productos_mas_vendidos_cuenta_unidades_y_no_filas(ventas):
    assert productos_mas_vendidos(ventas, 1).to_dict() == {"Gel energético": 4}


def test_tallas_rechaza_categorias_que_no_son_zapatillas(ventas):
    with pytest.raises(ValueError):
        tallas_mas_vendidas(ventas, "Geles y electrolitos")


def test_marcas_calcula_porcentaje_de_segunda_mano(ventas):
    hoka = marcas_de_zapatillas(ventas).loc["Hoka"]
    assert hoka["unidades"] == 2
    assert hoka["porcentaje_segunda"] == 50.0
