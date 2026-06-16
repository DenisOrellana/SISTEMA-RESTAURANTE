# 🚀 GUÍA RÁPIDA DE INICIO

## ¿Cómo ejecutar la aplicación?

### Paso 1: Verificar Python
```bash
python --version
# Deberá mostrar Python 3.6 o superior
```

### Paso 2: Ejecutar la Aplicación
```bash
# En Windows
python restaurante_app.py

# En macOS/Linux
python3 restaurante_app.py
```

## 📱 Interfaz Principal

La ventana se divide en 4 partes:

```
┌─────────────────────────────────────────────────────────┐
│  🍽️ Sistema de Gestión de Restaurante                  │
├─────────────────────────────────────────────────────────┤
│  │                                                      │
│  │ Barra Lateral   │  Catálogo de Menú  │  Vista Previa│
│  │ - Control..     │  ┌─────────────┐   │  de Orden    │
│  │ - Catálogo      │  │ PLATILLOS   │   │  ┌────────┐  │
│  │ - Confirmación  │  │ BEBIDAS     │   │  │        │  │
│  │ - Historial     │  ├─────────────┤   │  │ Items  │  │
│  │ - Configuración │  │ [Tarjetas]  │   │  │        │  │
│  │                 │  │ [Tarjetas]  │   │  │ Total: │  │
│  │                 │  │ [Scroll]    │   │  │        │  │
│  │                 │  │             │   │  └────────┘  │
│  │                 │  │             │   │              │
│  └─────────────────┴─────────────────┘───┘──────────────┘
```

## 🍽️ Crear una Orden Paso a Paso

### 1️⃣ Selecciona Productos
- Ve a la sección "Catálogo de Menú" (debe estar activa por defecto)
- Elige entre **PLATILLOS** o **BEBIDAS** (pestañas superiores)
- Haz clic en el botón **➕** de cualquier producto

**Ejemplo:**
```
Paso 1: Haz clic en ➕ de "Filete Mignon"
        ↓ Aparece en "Vista Previa de Orden" → Filete Mignon x1
        
Paso 2: Haz clic en ➕ de "Agua Mineral"
        ↓ Se agrega → Agua Mineral x1
        
Paso 3: Haz clic nuevamente en ➕ de "Agua Mineral"
        ↓ Aumenta cantidad → Agua Mineral x2
```

### 2️⃣ Ingresa Datos de la Orden
En el panel derecho "Vista Previa de Orden":
- **Mesa**: Ingresa el número de mesa (ej: 5)
- **Comensales**: Ingresa cantidad de personas (ej: 4)

```
┌─────────────────────┐
│ Vista Previa Orden  │
│ ────────────────────│
│ Filete Mignon x1    │
│   $24.99            │
│ Agua Mineral x2     │
│    $5.00            │
│ ────────────────────│
│ Total: $29.99       │
│                     │
│ Mesa: [5]           │ ← Ingresa aquí
│ Comensales: [4]     │ ← Y aquí
│ [✓ Confirmar]       │
│ [🗑️ Limpiar]        │
└─────────────────────┘
```

### 3️⃣ Confirma la Orden
- Haz clic en el botón **✓ Confirmar Orden**
- Aparecerá un mensaje: "Orden #1 guardada correctamente para la mesa 5"
- ✅ Los datos se guardan en `restaurante_db.txt`

### 4️⃣ Ver Órdenes Guardadas
- Navega a **"Confirmación de Orden"** en la barra lateral
- Verás la tabla de todas las órdenes guardadas
- O ve a **"Historial y Control"** para una vista completa

## 📋 Opciones del Menú (Barra Lateral)

### 🪑 Control de Mesas
- Vista de 16 mesas organizadas en grid (4x4)
- Permite visualizar el estado de cada mesa
- Click en una mesa para más detalles

### 🍽️ Catálogo de Menú (Activo por defecto)
- Listado de productos disponibles
- Opciones: **PLATILLOS** y **BEBIDAS**
- Agregar a la orden con el botón ➕

### ✓ Confirmación de Orden
- Muestra todas las órdenes que se han confirmado
- Formato: ID | Mesa | Comensales | Items | Total
- Botón para refrescar la lista

### 📊 Historial y Control
- Tabla completa con todas las transacciones
- Información más detallada de cada orden
- Útil para análisis y reportes

### ⚙️ Configuración
- Información del sistema
- Opciones de exportación y reinicio
- Diálogo "Acerca De"

## 🎨 Personalización Rápida

### Cambiar el Nombre del Restaurante
```python
# En restaurante_app.py, busca:
titulo = tk.Label(
    header,
    text="🍽️ Platillos / Bebidas",  # ← Cambia aquí
```

### Cambiar Colores
```python
# En restaurante_app.py, busca la clase Colores:
class Colores:
    ACENTO_NARANJA = "#FF9F43"      # ← Cambiar aquí por otro color
    FONDO_PRINCIPAL = "#F5F5F5"     # ← O aquí
```

Colores sugeridos:
- Azul profesional: `#3498DB`
- Verde moderno: `#27AE60`
- Rojo llamativo: `#E74C3C`
- Púrpura elegante: `#9B59B6`

### Agregar Nuevos Productos
```python
# En restaurante_app.py, busca CatalogoComienzo.obtener_productos():
"Entradas": [
    Producto(1, "Alitas Picantes", "Alitas crujientes...", 8.99, "Entradas"),
    Producto(2, "Camarones...", "Camarones...", 12.50, "Entradas"),
    # Agrega aquí tu nuevo producto:
    Producto(99, "Mi Nuevo Plato", "Descripción", 15.99, "Entradas"),
],
```

## 💾 Base de Datos (restaurante_db.txt)

Ejemplo de archivo guardado:

```
1|5|4|Filete Mignonx1;Agua Mineralx2|29.99
2|3|2|Pechuga Rellenax1;Refresco|19.50
3|8|6|Salmón a la Mantequillax2;Vino Tintox1|69.97
```

**Estructura:**
- `ID` = Número de orden (secuencial)
- `Mesa` = Número de mesa
- `Comensales` = Cantidad de personas
- `Items` = Productos con cantidad (separados por ;)
- `Total` = Suma total de la orden

## ⌨️ Atajos Útiles

| Acción | Cómo Hacerlo |
|--------|-------------|
| Agregar producto | Click en ➕ |
| Eliminar item de orden | Click en ✕ en Vista Previa |
| Limpiar toda la orden | Click en 🗑️ Limpiar |
| Confirmar orden | Click en ✓ Confirmar (Mesa + Comensales requeridos) |
| Cambiar pestaña | Click en PLATILLOS o BEBIDAS |
| Navegar secciones | Click en botones de barra lateral |
| Refrescar órdenes | Click en 🔄 Refrescar |

## 🐛 Problemas Comunes

### La aplicación no inicia
**Solución:**
```bash
# Verifica Python
python --version

# Si no está instalado, descárgalo desde https://www.python.org
# ⚠️ Marca "Add Python to PATH" durante instalación
```

### Error: "No module named 'tkinter'"
**Solución Windows:**
- Desinstala Python
- Reinstala marcando la opción "tcl/tk and IDLE"

**Solución Linux:**
```bash
sudo apt-get install python3-tk
```

**Solución macOS:**
```bash
brew install python-tk@3.11  # (reemplaza 3.11 por tu versión)
```

### Los colores no se ven correctamente
- Actualiza tu tema del SO a "Modo Claro" (Light Mode)
- Los colores están optimizados para fondo claro

### La ventana es muy pequeña/grande
En `restaurante_app.py`, busca:
```python
self.root.geometry("1400x750")  # Ancho x Alto
# Cambia a tus preferencias, ej:
self.root.geometry("1600x900")
```

## 📊 Estadísticas de Demostración

Para probar rápidamente, crea estas órdenes:

```
Orden 1:
  Mesa: 1, Comensales: 2
  + Alitas Picantes x2
  + Agua Mineral x2
  Total esperado: $25.98

Orden 2:
  Mesa: 3, Comensales: 4
  + Filete Mignon x1
  + Pechuga Rellena x2
  + Bebida x1
  Total esperado: $57.98
```

## 🎓 Conceptos Implementados

✅ **Tkinter** - GUI Framework
✅ **POO** - Clases y Objetos
✅ **Dataclasses** - Estructuras de datos
✅ **Archivos** - Lectura/Escritura
✅ **Eventos** - Manejo de clics y hover
✅ **Validación** - Entrada de datos
✅ **Interfaz Responsiva** - Layouts y packing

## 📞 Soporte

Para más información:
- Lee `README.md`
- Revisa los comentarios en `restaurante_app.py`
- Consulta la documentación de Tkinter: https://docs.python.org/3/library/tkinter.html

---

¡Disfruta del Sistema de Gestión de Restaurante! 🍽️

