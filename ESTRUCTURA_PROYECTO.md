# 🏗️ ESTRUCTURA Y ARQUITECTURA DEL PROYECTO

## 📁 Archivos del Proyecto

```
SISTEMA RESTAURANTE/
│
├── restaurante_app.py              # 🎯 ARCHIVO PRINCIPAL (Aplicación completa)
├── configuracion.py                # ⚙️  Archivo de configuración personalizable
├── restaurante_db.txt              # 💾 Base de datos (se crea automáticamente)
├── ejemplo_datos.txt               # 📊 Datos de ejemplo para demostración
│
├── README.md                       # 📖 Documentación completa
├── INICIO_RAPIDO.md                # 🚀 Guía rápida de inicio
├── ESTRUCTURA_PROYECTO.md          # 🏗️  Este archivo
│
└── .gitignore (opcional)           # Git (ignorar archivos temporales)
```

## 🏛️ Arquitectura del Código

### Flujo Principal

```
┌─────────────────────────────────────────────────┐
│    main() - Punto de Entrada                    │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│  AplicacionRestaurante (Clase Principal)        │
│  - Coordina toda la aplicación                  │
│  - Gestiona navegación                          │
│  - Conecta componentes                          │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌────────┐   ┌────────┐   ┌─────────┐
   │Sidebar │   │Catalogo│   │VistaPrevia
   │        │   │Menú    │   │ Orden
   │Naveg.  │   │        │   │
   └────────┘   └────────┘   └─────────┘
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
        ┌───────────────────────┐
        │  BaseDatos (Archivo)  │
        │  restaurante_db.txt   │
        └───────────────────────┘
```

## 📦 Componentes Principales

### 1. **Colores** (Enum de Colores)
```
│
├── ACENTO_NARANJA          → #FF9F43 (Color principal)
├── FONDO_PRINCIPAL         → #F5F5F5 (Gris claro)
├── FONDO_TARJETAS          → #FFFFFF (Blanco)
├── NARANJA_CLARO           → #FFEAD2 (Hover effect)
├── NARANJA_OSCURO          → #E67E22 (Click effect)
├── TEXTO_OSCURO            → #2C3E50
├── BORDE_GRIS              → #E0E0E0
└── GRIS_INACTIVO           → #BDC3C7
```

### 2. **Dataclasses** (Estructuras de Datos)

#### Producto
```python
@dataclass
class Producto:
    id: int                    # Identificador único (1-15)
    nombre: str               # Nombre del platillo
    descripcion: str          # Descripción corta
    precio: float             # Precio en pesos
    categoria: str            # Entradas, Fuerte, Postre, Bebidas
    cantidad: int = 0         # Se agrega dinámicamente
```

#### Orden
```python
@dataclass
class Orden:
    id_orden: int             # ID única (secuencial)
    mesa: int                 # Número de mesa (1-20)
    comensales: int           # Cantidad de personas
    items: list               # [(Producto, cantidad), ...]
    total: float              # Suma total
    fecha: str                # Timestamp
    
    def a_txt():              # Convertir a formato archivo
        # ID|Mesa|Comensales|Items|Total
```

### 3. **BaseDatos** (Gestión de Persistencia)
```
BaseDatos
├── guardar_orden(orden)     → Escribe en restaurante_db.txt
└── obtener_ordenes()        → Lee del archivo
```

**Flujo:**
```
[Confirmar Orden] → [Crear Orden] → [BaseDatos.guardar_orden()] → [archivo.txt]
```

### 4. **CatalogoComienzo** (Datos Estáticos)
```
CatalogoComienzo
│
├── obtener_productos()
│   │
│   └── Retorna diccionario con:
│       │
│       ├── PLATILLOS
│       │   ├── Entradas (3 productos)
│       │   ├── Fuerte (4 productos)
│       │   └── Postre (3 productos)
│       │
│       └── BEBIDAS
│           └── Bebidas (5 productos)
```

### 5. **BarraLateral** (Navegación)
```
BarraLateral (tk.Frame)
├── Logo/Título
├── Separador
├── Botones de Navegación
│   ├── Control de Mesas
│   ├── Catálogo de Menú      [ACTIVO POR DEFECTO]
│   ├── Confirmación de Orden
│   ├── Historial y Control
│   └── Configuración
│
└── Callbacks:
    └── on_select(codigo_seccion)
```

**Estados de Botones:**
- Inactivo: Fondo blanco, texto gris
- Activo: Fondo naranja claro, texto naranja
- Hover: Cambia a naranja claro

### 6. **TarjetaProducto** (Componente Visual)
```
┌────────────────────┐
│  [Imagen Emoji]    │  ← Frame naranja
├────────────────────┤
│ Nombre Producto    │  ← Label (negrita)
│ Descripción...     │  ← Label (gris, pequeño)
├────────────────────┤
│ $XX.XX      ➕     │  ← Precio + Botón
└────────────────────┘

Eventos:
└── on_agregar_callback()
    └── Agrega a VistaPreviaOrden
```

### 7. **CatalogoMenu** (Sección Principal)
```
CatalogoMenu (tk.Frame)
├── Header (naranja)
├── ttk.Notebook (Pestañas)
│   ├── PLATILLOS
│   │   └── Scroll Container
│   │       ├── Columna 1: Entradas [Tarjetas]
│   │       ├── Columna 2: Fuerte [Tarjetas]
│   │       └── Columna 3: Postre [Tarjetas]
│   │
│   └── BEBIDAS
│       └── Scroll Container
│           └── Bebidas [Tarjetas]
```

### 8. **VistaPreviaOrden** (Panel Derecho)
```
VistaPreviaOrden (tk.Frame)
├── Header (naranja)
├── Scroll Container
│   └── Items dinámicos
│       ├── Nombre x Cantidad
│       ├── Subtotal
│       └── Botón ✕ (eliminar)
├── Separator
├── Totales
│   └── Total: $XX.XX
├── Formulario
│   ├── Mesa: [Entry]
│   └── Comensales: [Entry]
├── Botón: ✓ Confirmar
└── Botón: 🗑️ Limpiar
```

**Métodos:**
- `agregar_producto(producto)` - Suma items
- `_actualizar_vista()` - Recalcula total
- `_eliminar_producto(producto)` - Quita items
- `_confirmar_orden()` - Guarda en BD

### 9. **ControlMesas** (Sección de Mesas)
```
ControlMesas (tk.Frame)
├── Header
└── Grid 4x4
    └── 16 Botones (Mesa 1-16)
```

### 10. **ConfirmacionOrden** (Sección de Confirmación)
```
ConfirmacionOrden (tk.Frame)
├── Header
├── ScrolledText (área de lectura)
│   └── Muestra: ID | Mesa | Comensales | Items | Total
└── Botón: 🔄 Refrescar
```

### 11. **HistorialControl** (Sección de Historial)
```
HistorialControl (tk.Frame)
├── Header
└── ttk.Treeview
    ├── Columna: ID
    ├── Columna: Mesa
    ├── Columna: Comensales
    ├── Columna: Items
    └── Columna: Total
```

### 12. **Configuracion** (Sección de Config)
```
Configuracion (tk.Frame)
├── Header
├── Frame: Información del Sistema
│   ├── Versión
│   ├── Tipo BD
│   ├── Formato
│   └── Estado
└── Frame: Opciones
    ├── Botón: 📤 Exportar
    ├── Botón: 🔄 Reiniciar BD
    └── Botón: ℹ️  Acerca De
```

### 13. **AplicacionRestaurante** (Controlador Principal)
```
AplicacionRestaurante
├── __init__()
│   ├── Crear ventana
│   ├── Inicializar BaseDatos
│   ├── Crear BarraLateral
│   └── Crear todas las secciones
│
├── _crear_secciones()
│   ├── ControlMesas
│   ├── CatalogoMenu + VistaPreviaOrden
│   ├── ConfirmacionOrden
│   ├── HistorialControl
│   └── Configuracion
│
├── _on_nav_select(codigo)
│   └── Mostrar/ocultar secciones
│
├── _agregar_a_orden(producto)
│   └── Delegar a VistaPreviaOrden
│
└── _confirmar_orden(mesa, comensales, items, total)
    ├── Crear Orden
    ├── Guardar en BaseDatos
    └── Mostrar confirmación
```

## 🔄 Flujo de Datos

### Agregar Producto a Orden
```
[Click ➕] 
    ↓
[TarjetaProducto._agregar_producto()]
    ↓
[on_agregar_callback(producto)]
    ↓
[AplicacionRestaurante._agregar_a_orden(producto)]
    ↓
[VistaPreviaOrden.agregar_producto(producto)]
    ↓
[VistaPreviaOrden._actualizar_vista()]
    ↓
[Recalcular total y mostrar]
```

### Confirmar Orden
```
[Click ✓ Confirmar]
    ↓
[VistaPreviaOrden._confirmar_orden()]
    ↓
[Validar mesa, comensales, items]
    ↓
[AplicacionRestaurante._confirmar_orden()]
    ↓
[Crear: Orden(id, mesa, comensales, items, total)]
    ↓
[BaseDatos.guardar_orden(orden)]
    ↓
[Escribir en restaurante_db.txt]
    ↓
[Mostrar mensaje de éxito]
    ↓
[Limpiar VistaPreviaOrden]
```

### Leer Órdenes
```
[Click "Historial y Control"]
    ↓
[HistorialControl._cargar_historial()]
    ↓
[BaseDatos.obtener_ordenes()]
    ↓
[Leer restaurante_db.txt]
    ↓
[Parsear líneas (ID|Mesa|...)]
    ↓
[Mostrar en ttk.Treeview]
```

## 📊 Modelos de Datos

### Orden Ejemplo
```
Objeto Python:
Orden(
    id_orden=1,
    mesa=5,
    comensales=4,
    items=[
        (Producto(nombre="Filete Mignon", precio=24.99), 1),
        (Producto(nombre="Agua Mineral", precio=2.50), 2)
    ],
    total=29.99,
    fecha="2026-06-16 14:30:00"
)

Guardado en archivo:
1|5|4|Filete Mignonx1;Agua Mineralx2|29.99
```

## 🎯 Patrones de Diseño

### 1. **Model-View-Controller (MVC)**
- **Model**: Producto, Orden, BaseDatos
- **View**: TarjetaProducto, VistaPreviaOrden, BarraLateral
- **Controller**: AplicacionRestaurante

### 2. **Observador (Observer)**
- Callbacks: `on_agregar_callback`, `on_confirmar_callback`
- BarraLateral usa callbacks para notificar cambios

### 3. **Factory (Implícito)**
- CatalogoComienzo genera productos

### 4. **Singleton**
- BaseDatos (única instancia por aplicación)
- AplicacionRestaurante

## ⚙️ Tecnologías Utilizadas

| Tecnología | Propósito |
|-----------|----------|
| **Python 3.6+** | Lenguaje base |
| **tkinter** | GUI Framework |
| **tkinter.ttk** | Widgets modernos (Notebook, Treeview, Style) |
| **dataclasses** | Estructuras de datos tipadas |
| **pathlib** | Manejo de archivos |
| **datetime** | Timestamps |
| **json** | Potencial para futuras migraciones |

## 📈 Escalabilidad

### Mejoras Futuras

1. **Base de Datos SQL**
   ```
   BaseDatos (Abstract)
   ├── BaseDatosArchivo
   └── BaseDatosSQLite/PostgreSQL
   ```

2. **Autenticación**
   ```
   Usuario (dataclass)
   └── AplicacionRestaurante(usuario)
   ```

3. **Reportes**
   ```
   ReportesVentas
   ├── diario()
   ├── semanal()
   └── mensual()
   ```

4. **API REST**
   ```
   FastAPI
   ├── GET /ordenes
   ├── POST /ordenes
   └── GET /ordenes/{id}
   ```

## 🔍 Validación y Seguridad

### Validaciones Implementadas
✅ Mesa entre 1 y 20
✅ Comensales entre 1 y 20
✅ Orden no vacía antes de confirmar
✅ Manejo de excepciones en archivo I/O

### Mejoras de Seguridad
- Encriptación de datos sensibles
- Logs de auditoría
- Control de acceso por usuario
- Validación SQL injection prevention

## 📚 Recursos

- **Documentación Tkinter**: https://docs.python.org/3/library/tkinter.html
- **ttk.Notebook**: https://docs.python.org/3/library/tkinter.ttk.html
- **Dataclasses**: https://docs.python.org/3/library/dataclasses.html

---

**Creado**: 2026-06-16
**Versión**: 1.0.0
**Estado**: Producción ✅

