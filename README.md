# Análisis de ventas de AmazonFit Store

Programa en Python que analiza las ventas de **AmazonFit Store**, una tienda ficticia de artículos de running y trail en Tena, Ecuador. Calcula los ingresos por categoría y por mes, los productos más vendidos, las tallas de zapatillas más pedidas y qué marcas se venden más de segunda mano.

El repositorio contiene dos versiones del mismo análisis:

- `original/`: el programa inicial, con malas prácticas de legibilidad, redundancia y rendimiento. Se conserva solo para comparar.
- `amazonfit/` y `main.py`: la versión corregida, modular, documentada y con pruebas.

> Los datos de ventas son simulados con fines académicos.

## Requisitos

- Python 3.10 o superior
- Las librerías de `requirements.txt`

## Instalación

```bash
git clone https://github.com/arieljmnz11/amazonfit-ventas.git
cd amazonfit-ventas
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux o macOS
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Uso

Generar de nuevo el archivo de ventas, que siempre produce los mismos datos:

```bash
python scripts/generar_datos.py
```

Generar el reporte:

```bash
python main.py
```

Ver mensajes de depuración o analizar otro archivo:

```bash
python main.py --detalle
python main.py --datos ruta/a/otro_archivo.csv
```

Comparar la versión original con la optimizada:

```bash
python scripts/comparar_rendimiento.py
python scripts/micro_comparaciones.py
```

## Estructura del proyecto

```text
amazonfit-ventas/
├── amazonfit/                  Paquete con la lógica del análisis
│   ├── config.py               Constantes, rutas y tipos de columnas
│   ├── carga.py                Lectura del CSV, completa o por bloques
│   ├── limpieza.py             Duplicados, precios vacíos y categorías
│   ├── metricas.py             Cálculos vectorizados con pandas
│   └── reportes.py             Armado del reporte de texto
├── datos/ventas_amazonfit.csv  Ventas simuladas, 201 200 filas
├── original/                   Programa inicial sin corregir
├── scripts/                    Generación de datos y comparaciones
├── tests/                      Pruebas unitarias y de integración
├── main.py                     Punto de entrada
├── requirements.txt            Dependencias para ejecutar
└── requirements-dev.txt        Dependencias para desarrollar y probar
```

## Columnas del archivo de ventas

| Columna | Descripción |
|---|---|
| `id_venta` | Código único de la venta |
| `fecha` | Fecha en formato AAAA-MM-DD |
| `categoria` | Por ejemplo Zapatillas de trail o Geles y electrolitos |
| `producto` | Nombre del producto o modelo |
| `marca` | Marca, o Sin marca para productos genéricos |
| `talla` | Talla europea en zapatillas, S a XL en ropa, Única en el resto |
| `condicion` | Nueva o Segunda mano |
| `cantidad` | Unidades vendidas |
| `precio_unitario` | Precio por unidad en dólares |
| `metodo_pago` | Efectivo, Transferencia o Tarjeta. El efectivo tiene 5 % de descuento |
| `canal` | Tienda, WhatsApp o Instagram |

## Pruebas y calidad

```bash
pytest                        # pruebas unitarias y de integración
pytest --cov=amazonfit        # pruebas con cobertura
ruff check .                  # estilo PEP 8 y docstrings PEP 257
```

GitHub Actions ejecuta Ruff y las pruebas en cada push y en cada pull request hacia `main`.

## Cómo contribuir

1. Crear una rama desde `main`, por ejemplo `feature/ventas-por-canal`.
2. Escribir el código con docstrings y su prueba.
3. Verificar que `ruff check .` y `pytest` pasen.
4. Abrir un pull request hacia `main`.
