# 🍽️ Sistema de Gestión de Restaurante

## Descripción
Sistema completo de gestión de restaurante con interfaz gráfica moderna desarrollado en **Python 3.x + Tkinter** (sin dependencias externas).

## Características Principales

### 🎨 Diseño Visual
- Interfaz moderna con **Flat Design**
- Paleta de colores profesional:
  - Color acento: **Naranja/Ámbar (#FF9F43)**
  - Fondo: **Gris claro (#F5F5F5)**
  - Tarjetas: **Blanco puro (#FFFFFF)**
- Efectos hover en botones e interactivos
- Responsive y bien estructurado

### 📋 Módulos

#### 1. **Control de Mesas**
- Grid de 16 mesas (4x4)
- Visualización rápida del estado

#### 2. **Catálogo de Menú** (Principal)
- 2 pestañas: **PLATILLOS** y **BEBIDAS**
- 16 productos con:
  - Imagen simulada (emoji)
  - Nombre y descripción
  - Precio destacado
  - Botón "+" para agregar
- Scroll vertical para navegación

#### 3. **Vista Previa de Orden** (Panel Derecho)
- Listado dinámico de items agregados
- Cálculo automático de totales
- Campos para **Mesa** y **Comensales**
- Botones: Confirmar y Limpiar
- Eliminación individual de items

#### 4. **Confirmación de Orden**
- Tabla de órdenes guardadas
- Formato: ID | Mesa | Comensales | Items | Total
- Botón para refrescar

#### 5. **Historial y Control**
- Tabla completa con todas las transacciones
- Visualización de datos históricos

#### 6. **Configuración**
- Información del sistema
- Opciones de exportación y reinicio
- Diálogo "Acerca De"

## 📦 Requisitos

```bash
# Solo se requiere Python 3.6+ (Tkinter incluido)
python --version  # Verificar versión
```

Tkinter generalmente viene preinstalado con Python. Si no está disponible:

### En Windows:
```bash
# Durante la instalación de Python, marcar "tcl/tk and IDLE"
# O reinstalar Python con esta opción
```

### En macOS:
```bash
brew install python-tk
```

### En Linux (Debian/Ubuntu):
```bash
sudo apt-get install python3-tk
```

## 🚀 Uso

### Ejecutar la aplicación:

```bash
python restaurante_app.py
```

### Funcionalidad Básica:

1. **Agregar Productos:**
   - Haz clic en el botón "➕" de cualquier producto
   - El item aparece en "Vista Previa de Orden"

2. **Modificar Orden:**
   - Aumenta la cantidad haciendo clic nuevamente
   - Elimina items con el botón "✕"
   - Limpia todo con "🗑️ Limpiar"

3. **Confirmar Orden:**
   - Completa los campos "Mesa" y "Comensales"
   - Haz clic en "✓ Confirmar Orden"
   - Los datos se guardan en `restaurante_db.txt`

4. **Ver Historial:**
   - Ve a "Historial y Control"
   - Observa todas las órdenes guardadas

## 📁 Estructura de Archivos

```
SISTEMA RESTAURANTE/
├── restaurante_app.py           # Aplicación principal (único archivo)
├── restaurante_db.txt           # Base de datos (se crea automáticamente)
└── README.md                    # Este archivo
```

## 💾 Formato de Base de Datos

Archivo: `restaurante_db.txt`

```
ID|Mesa|Comensales|Items|Total
1|1|4|Alitas Picantesx2;Filete Mignonx1|42.97
2|3|2|Pechuga Rellenax1;Agua Mineralx2|22.99
3|5|6|Salmón a la Mantequillax3;Bebidax1|73.96
```

**Separadores:**
- `|` entre campos
- `;` entre items
- `x` para cantidad

## 🎯 Clases Principales

### `Colores`
Define la paleta de colores del sistema.

### `Producto` (dataclass)
Estructura de datos para productos:
- `id`: Identificador único
- `nombre`: Nombre del platillo
- `descripcion`: Descripción corta
- `precio`: Precio en pesos
- `categoria`: Categoría del producto

### `Orden` (dataclass)
Estructura de datos para órdenes:
- `id_orden`: Identificador único
- `mesa`: Número de mesa
- `comensales`: Cantidad de comensales
- `items`: Lista de (producto, cantidad)
- `total`: Total de la orden
- `fecha`: Timestamp de creación

### `BaseDatos`
Gestiona la persistencia de datos en archivo de texto.

### `BarraLateral`
Componente de navegación izquierda con botones activos/inactivos.

### `TarjetaProducto`
Componente visual para cada producto (tarjeta con imagen, nombre, precio, botón).

### `CatalogoMenu`
Sección principal con pestañas y products en scroll.

### `VistaPreviaOrden`
Panel derecho con listado dinámico y confirmación de órdenes.

### `AplicacionRestaurante`
Clase principal que coordina toda la aplicación.

## 🎨 Personalización

### Cambiar Colores:
Edita la clase `Colores` en el archivo:

```python
class Colores:
    ACENTO_NARANJA = "#FF9F43"      # Cambiar aquí
    FONDO_PRINCIPAL = "#F5F5F5"     # O aquí
    # ... etc
```

### Agregar Productos:
Modifica la clase `CatalogoComienzo`:

```python
@staticmethod
def obtener_productos():
    productos = {
        "PLATILLOS": {
            "Entradas": [
                Producto(1, "Nuevo Plato", "Descripción", 12.50, "Entradas"),
                # ... más productos
            ]
        }
    }
```

### Cambiar Fuentes:
La fuente por defecto es `"Segoe UI"`. Para cambiar globalmente:

```python
# Busca "Segoe UI" y reemplaza con tu fuente preferida
# Opciones: "Helvetica", "Arial", "Courier New", "Times New Roman"
```

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'tkinter'`
```bash
# Windows (reinstalar Python con Tkinter)
# Linux: sudo apt-get install python3-tk
# macOS: brew install python-tk@3.11  # (reemplaza 3.11 con tu versión)
```

### La ventana se ve pequeña
```python
# Modifica la línea en AplicacionRestaurante.__init__():
self.root.geometry("1400x750")  # Ajusta según tu pantalla
```

### Los colores no se ven bien
Actualiza el gestor de temas del sistema operativo a modo claro (Light Mode).

## 📝 Ejemplo de Uso

```bash
$ python restaurante_app.py

# Se abre la aplicación gráfica
# 1. Haz clic en productos para agregarlos
# 2. Ingresa número de mesa y comensales
# 3. Haz clic en "Confirmar Orden"
# 4. Verifica en "Historial y Control"
```

## 🔐 Seguridad

- ✅ Validación de entrada en campos de mesa y comensales
- ✅ Validación de órdenes vacías
- ✅ Manejo de excepciones en lectura/escritura de archivos

## 📊 Estadísticas del Código

- **Líneas de código**: ~1000+
- **Clases**: 15+
- **Métodos**: 50+
- **Dependencias externas**: 0 (solo Python + Tkinter)

## 📈 Mejoras Futuras

- [ ] Conexión a base de datos SQL
- [ ] Sistema de autenticación de usuarios
- [ ] Reportes y estadísticas
- [ ] Exportación a PDF
- [ ] Sistema de caja registradora
- [ ] Gestión de inventario
- [ ] Historial de ganancias

## 📄 Licencia

Proyecto educativo. Libre para uso y modificación.

## 🎓 Autor

Sistema desarrollado como proyecto de educación en Python y desarrollo de interfaces gráficas.

---

**¿Preguntas?** Revisa el código comentado en `restaurante_app.py`

