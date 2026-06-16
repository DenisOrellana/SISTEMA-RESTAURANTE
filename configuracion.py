"""
Archivo de Configuración del Sistema de Gestión de Restaurante
Este archivo permite personalizar fácilmente el sistema sin modificar el código principal
"""

# ==================== CONFIGURACIÓN DE VENTANA ====================
VENTANA_TITULO = "🍽️ Sistema de Gestión de Restaurante"
VENTANA_ANCHO = 1400
VENTANA_ALTO = 750

# ==================== CONFIGURACIÓN DE FUENTES ====================
FUENTE_PRINCIPAL = "Segoe UI"         # Arial, Helvetica, Courier New, Times New Roman
FUENTE_SIZE_NORMAL = 10
FUENTE_SIZE_GRANDE = 11
FUENTE_SIZE_TITULO = 14
FUENTE_SIZE_PEQUEÑO = 8

# ==================== CONFIGURACIÓN DE COLORES ====================
# Colores principales
COLOR_ACENTO_NARANJA = "#FF9F43"
COLOR_FONDO_PRINCIPAL = "#F5F5F5"
COLOR_FONDO_TARJETAS = "#FFFFFF"
COLOR_NARANJA_CLARO = "#FFEAD2"
COLOR_NARANJA_OSCURO = "#E67E22"
COLOR_TEXTO_OSCURO = "#2C3E50"
COLOR_BORDE_GRIS = "#E0E0E0"
COLOR_GRIS_INACTIVO = "#BDC3C7"

# ==================== CONFIGURACIÓN DE PRODUCTOS ====================
# Número de mesas
NUMERO_MESAS = 16  # 4x4

# Productos por categoría
PRODUCTOS = {
    "PLATILLOS": {
        "Entradas": [
            {"nombre": "Alitas Picantes", "desc": "Alitas crujientes con salsa picante casera", "precio": 8.99},
            {"nombre": "Camarones Empanizados", "desc": "Camarones frescos empanizados al horno", "precio": 12.50},
            {"nombre": "Tabla de Quesos", "desc": "Selección de quesos artesanales importados", "precio": 14.99},
        ],
        "Fuerte": [
            {"nombre": "Filete Mignon", "desc": "Filete de res de 250g con champiñones", "precio": 24.99},
            {"nombre": "Pechuga Rellena", "desc": "Pechuga de pollo rellena de jamón y queso", "precio": 16.50},
            {"nombre": "Pasta Alfredo", "desc": "Pasta fresca con salsa cremosa de champiñones", "precio": 14.99},
            {"nombre": "Salmón a la Mantequilla", "desc": "Salmón fresco con salsa de vino blanco", "precio": 22.99},
        ],
        "Postre": [
            {"nombre": "Brownie de Chocolate", "desc": "Brownie casero con helado de vainilla", "precio": 7.99},
            {"nombre": "Flan Napolitano", "desc": "Flan casero con caramelo crujiente", "precio": 6.99},
            {"nombre": "Cheesecake Clásico", "desc": "Cheesecake de Nueva York con frutos rojos", "precio": 9.50},
        ],
    },
    "BEBIDAS": {
        "Bebidas": [
            {"nombre": "Agua Mineral", "desc": "Botella de agua mineral 500ml", "precio": 2.50},
            {"nombre": "Refresco", "desc": "Refresco surtido 330ml", "precio": 3.00},
            {"nombre": "Jugo Natural", "desc": "Jugo recién exprimido de frutas frescas", "precio": 5.99},
            {"nombre": "Vino Tinto", "desc": "Vino tinto reserva 2019", "precio": 22.99},
            {"nombre": "Cerveza Premium", "desc": "Cerveza artesanal local 355ml", "precio": 4.99},
        ],
    }
}

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================
ARCHIVO_BASE_DATOS = "restaurante_db.txt"
SEPARADOR_CAMPOS = "|"
SEPARADOR_ITEMS = ";"
SEPARADOR_CANTIDAD = "x"

# ==================== CONFIGURACIÓN DE MENSAJES ====================
MENSAJE_ORDEN_GUARDADA = "Orden #{} guardada correctamente para la mesa {}"
MENSAJE_ERROR_GUARDAR = "No se pudo guardar la orden"
MENSAJE_ORDEN_VACIA = "La orden está vacía"
MENSAJE_DATOS_INVALIDOS = "Por favor ingrese mesa y comensales válidos"

# ==================== CONFIGURACIÓN DE INTERFAZ ====================
# Tamaño de tarjetas de producto
TARJETA_ANCHO = 160
TARJETA_ALTO = 250

# Tamaño de paneles
BARRA_LATERAL_ANCHO = 150
VISTA_PREVIA_ANCHO = 200

# Padding y espaciados
PADDING_GENERAL = 10
PADDING_TARJETA = 5
PADDING_BOTONES = 15

# ==================== CONFIGURACIÓN DE FUNCIONALIDADES ====================
# Permitir agregar múltiples veces el mismo producto
PERMITIR_CANTIDAD = True

# Mostrar confirmación antes de limpiar orden
CONFIRMAR_LIMPIAR = True

# Mostrar confirmación antes de reiniciar base de datos
CONFIRMAR_REINICIAR_DB = True

# ==================== CONFIGURACIÓN DE VALIDACIÓN ====================
# Número máximo de comensales
MAX_COMENSALES = 20

# Número de mesas máximo en validación
MAX_MESA = 20

# Número mínimo de comensales
MIN_COMENSALES = 1

# Número mínimo de mesa
MIN_MESA = 1
