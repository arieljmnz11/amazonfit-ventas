"""Datos pequeños de ejemplo compartidos por las pruebas."""

import pandas as pd
import pytest


@pytest.fixture
def ventas_crudas() -> pd.DataFrame:
    """Seis filas con los mismos problemas que tiene el archivo real."""
    return pd.DataFrame(
        {
            "id_venta": ["V1", "V2", "V2", "V3", "V4", "V5"],
            "fecha": pd.to_datetime(
                ["2025-07-01", "2025-07-15", "2025-07-15", "2025-08-02", "2025-08-03", "2025-08-04"]
            ),
            "categoria": [
                "Zapatillas de trail", " ZAPATILLAS DE TRAIL ", " ZAPATILLAS DE TRAIL ",
                "Geles y electrolitos", "Zapatillas de asfalto", "Zapatillas de asfalto",
            ],
            "producto": ["Speedgoat 5", "Speedgoat 5", "Speedgoat 5", "Gel energético", "Clifton 9", "Clifton 9"],
            "marca": ["Hoka", "Hoka", "Hoka", "Sin marca", "Hoka", "Hoka"],
            "talla": ["41", "41", "41", "Única", "40", "40"],
            "condicion": ["Segunda mano", "Nueva", "Nueva", "Nueva", "Nueva", "Segunda mano"],
            "cantidad": pd.array([1, 1, 1, 4, 1, -1], dtype="Int64"),
            "precio_unitario": [55.0, 120.0, 120.0, 2.5, None, 50.0],
            "metodo_pago": ["Efectivo", "Tarjeta", "Tarjeta", "Transferencia", "Efectivo", "Efectivo"],
            "canal": ["Tienda", "WhatsApp", "WhatsApp", "Tienda", "Tienda", "Instagram"],
        }
    )
