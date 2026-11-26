"""Constantes del proyecto reunidas en un solo lugar."""

from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_PROYECTO / "datos" / "ventas_amazonfit.csv"

DESCUENTO_EFECTIVO = 0.05
"""Descuento que la tienda aplica cuando el cliente paga en efectivo."""

CATEGORIAS_CALZADO = frozenset({"Zapatillas de asfalto", "Zapatillas de trail"})

COLUMNAS_REQUERIDAS = (
    "id_venta", "fecha", "categoria", "producto", "marca", "talla",
    "condicion", "cantidad", "precio_unitario", "metodo_pago", "canal",
)

TIPOS_COLUMNAS = {
    "id_venta": "string",
    "categoria": "string",
    "producto": "string",
    "marca": "category",
    "talla": "string",
    "condicion": "category",
    "cantidad": "Int64",
    "precio_unitario": "float64",
    "metodo_pago": "category",
    "canal": "category",
}
