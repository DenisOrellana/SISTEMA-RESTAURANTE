# 🎓 EJERCICIOS Y TUTORIALES DE PERSONALIZACIÓN

## Nivel 1: Principiante 🟢

### Ejercicio 1.1: Cambiar el Nombre del Restaurante
**Objetivo:** Cambiar el título de la aplicación

**Pasos:**
1. Abre `restaurante_app.py`
2. Busca la línea: `self.root.title("🍽️ Sistema de Gestión de Restaurante")`
3. Cambia a: `self.root.title("🍽️ Mi Restaurante Especial")`
4. Guarda y ejecuta

**Resultado:** El título de la ventana debe cambiar ✅

### Ejercicio 1.2: Cambiar Colores Principales
**Objetivo:** Personalizar la paleta de colores

**Pasos:**
1. En `restaurante_app.py`, busca la clase `Colores`
2. Cambia `ACENTO_NARANJA = "#FF9F43"` a `ACENTO_NARANJA = "#3498DB"` (azul)
3. Guarda y ejecuta

**Colores sugeridos para probar:**
- Verde: `#27AE60`
- Rojo: `#E74C3C`
- Púrpura: `#9B59B6`
- Naranja intenso: `#FF6B35`

**Resultado:** Todos los elementos naranjas ahora deben ser azules ✅

### Ejercicio 1.3: Cambiar Fuente Global
**Objetivo:** Usar una fuente diferente en toda la aplicación

**Pasos:**
1. En `restaurante_app.py`, usa Find & Replace (Ctrl+H)
2. Busca: `"Segoe UI"`
3. Reemplaza con: `"Arial"` o `"Helvetica"`
4. Haz "Replace All"
5. Guarda y ejecuta

**Resultado:** La fuente debe cambiar en toda la interfaz ✅

### Ejercicio 1.4: Agregar Nuevo Producto
**Objetivo:** Agregar un nuevo platillo al catálogo

**Pasos:**
1. En `restaurante_app.py`, busca `class CatalogoComienzo`
2. Encuentra la sección `"Fuerte":`
3. Agrega una línea nueva:
```python
"Fuerte": [
    Producto(4, "Filete Mignon", "Filete de res de 250g...", 24.99, "Fuerte"),
    # ... otros productos ...
    Producto(20, "Pulpo a la Gallega", "Pulpo fresco con paprika", 18.99, "Fuerte"),  # ← NUEVA
],
```
4. Guarda y ejecuta

**Resultado:** El nuevo producto debe aparecer en la columna "Fuerte" ✅

---

## Nivel 2: Intermedio 🟡

### Ejercicio 2.1: Cambiar Tamaño de Ventana
**Objetivo:** Adaptar la aplicación a tu resolución

**Pasos:**
1. En `restaurante_app.py`, busca `self.root.geometry("1400x750")`
2. Para pantalla más grande: `self.root.geometry("1920x1080")`
3. Para pantalla pequeña: `self.root.geometry("1000x600")`
4. Guarda y ejecuta

**Cálculo:** `Ancho x Alto` (en píxeles)

**Resultado:** La ventana debe tener el nuevo tamaño ✅

### Ejercicio 2.2: Cambiar Número de Mesas
**Objetivo:** Modificar la cantidad de mesas del restaurante

**Pasos:**
1. En `restaurante_app.py`, busca la clase `ControlMesas`
2. Encuentra la línea: `for mesa in range(1, 17):  # 16 mesas`
3. Cambia a: `for mesa in range(1, 25):  # 24 mesas`
4. Guarda y ejecuta

**Resultado:** Deberás ver más mesas en el grid ✅

### Ejercicio 2.3: Agregar Nueva Categoría
**Objetivo:** Crear una nueva categoría de platillos

**Pasos:**
1. En `restaurante_app.py`, busca `CatalogoComienzo.obtener_productos()`
2. En la sección "PLATILLOS", agrega:
```python
"PLATILLOS": {
    "Entradas": [ ... ],
    "Fuerte": [ ... ],
    "Postre": [ ... ],
    "Especiales": [  # ← NUEVA CATEGORÍA
        Producto(50, "Langosta Termidor", "Langosta fresca...", 42.99, "Especiales"),
        Producto(51, "Foie Gras", "Foie gras importado...", 38.99, "Especiales"),
    ],
},
```

3. En `CatalogoMenu._crear_contenido_platillos()`, actualiza el loop:
```python
categorias = ["Entradas", "Fuerte", "Postre", "Especiales"]  # ← Agregar
```

4. Guarda y ejecuta

**Resultado:** Nueva columna "Especiales" en el catálogo ✅

### Ejercicio 2.4: Cambiar Mensaje de Confirmación
**Objetivo:** Personalizar los mensajes de la aplicación

**Pasos:**
1. En `restaurante_app.py`, busca el método `_confirmar_orden`
2. Encuentra: `messagebox.showinfo("Éxito", ...)`
3. Cambia el mensaje:
```python
messagebox.showinfo("✓ Orden Confirmada", 
                   f"La orden #{id_orden} para la mesa {mesa} ha sido registrada exitosamente!\n\nTotal: ${total:.2f}")
```

4. Guarda y ejecuta

**Resultado:** El mensaje de confirmación debe ser más detallado ✅

---

## Nivel 3: Avanzado 🔴

### Ejercicio 3.1: Agregar Sistema de Descuentos
**Objetivo:** Implementar descuentos en órdenes

**Pasos:**

1. En `restaurante_app.py`, modifica la clase `VistaPreviaOrden`:
```python
def __init__(self, parent, on_confirmar_callback):
    # ... código existente ...
    self.descuento_porcentaje = 0.0  # ← AGREGAR
```

2. En `_crear_interfaz()`, agrega campo de descuento:
```python
tk.Label(formulario_frame, text="Descuento (%):", ...).grid(row=2, column=0)
self.entry_descuento = tk.Entry(formulario_frame, ...)
self.entry_descuento.grid(row=2, column=1)
```

3. En `_actualizar_vista()`, recalcula con descuento:
```python
self.total = 0.0
for producto, cantidad in self.items_orden.items():
    subtotal = producto.precio * cantidad
    self.total += subtotal

# Aplicar descuento
try:
    descuento = float(self.entry_descuento.get()) / 100
    self.total = self.total * (1 - descuento)
except:
    pass

self.label_total.config(text=f"${self.total:.2f}")
```

4. Guarda y ejecuta

**Resultado:** Deberías poder ingresar descuentos ✅

### Ejercicio 3.2: Agregar Búsqueda de Productos
**Objetivo:** Implementar un campo de búsqueda

**Pasos:**

1. En `restaurante_app.py`, modifica `CatalogoMenu._crear_interfaz()`:
```python
# Agregar ANTES del Notebook:
search_frame = tk.Frame(self.frame, bg=Colores.FONDO_PRINCIPAL)
search_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

tk.Label(search_frame, text="🔍 Buscar:", bg=Colores.FONDO_PRINCIPAL).pack(side=tk.LEFT)

self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=30)
self.search_entry.pack(side=tk.LEFT, padx=10)
self.search_entry.bind("<KeyRelease>", self._filtrar_productos)
```

2. Agrega el método de filtrado:
```python
def _filtrar_productos(self, event):
    termino = self.search_entry.get().lower()
    for tarjeta_id, tarjeta in self.tarjetas.items():
        if termino in tarjeta.producto.nombre.lower() or termino in tarjeta.producto.descripcion.lower():
            tarjeta.frame.pack(pady=5, fill=tk.X)
        else:
            tarjeta.frame.pack_forget()
```

3. Guarda y ejecuta

**Resultado:** Un campo de búsqueda funcional ✅

### Ejercicio 3.3: Guardar Backup de Base de Datos
**Objetivo:** Crear copias de seguridad automáticas

**Pasos:**

1. En `restaurante_app.py`, modifica `BaseDatos`:
```python
from datetime import datetime
from pathlib import Path
import shutil

def crear_backup(self):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(f"backups/restaurante_db_{timestamp}.txt")
        backup_path.parent.mkdir(exist_ok=True)
        shutil.copy(self.ruta, backup_path)
        return True
    except:
        return False
```

2. En `_confirmar_orden()`, llama al backup:
```python
if self.db.guardar_orden(orden):
    self.db.crear_backup()  # ← AGREGAR
    messagebox.showinfo(...)
```

3. Guarda y ejecuta

**Resultado:** Se crearán carpetas de backup automáticamente ✅

### Ejercicio 3.4: Añadir Funcionalidad de Exportación CSV
**Objetivo:** Exportar órdenes a CSV

**Pasos:**

1. En `restaurante_app.py`, agrega a `BaseDatos`:
```python
import csv

def exportar_csv(self, archivo_salida="ordenes_exportadas.csv"):
    try:
        ordenes = self.obtener_ordenes()
        with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Mesa", "Comensales", "Items", "Total"])
            for orden in ordenes:
                writer.writerow(orden.split("|"))
        return True
    except:
        return False
```

2. En `Configuracion._crear_interfaz()`, modifica botón de exportación:
```python
btn_export = tk.Button(
    opt_frame,
    text="📤 Exportar a CSV",
    command=self._exportar_csv  # ← AGREGAR
    ...
)

def _exportar_csv(self):
    # Acceder a la BD desde aquí (requiere referencia)
    pass
```

3. Guarda y ejecuta

**Resultado:** Botón de exportación funcional ✅

---

## Nivel 4: Experto 🟣

### Ejercicio 4.1: Sistema de Usuarios
**Objetivo:** Agregar login y roles de usuario

**Pasos:**

1. Crea clase `Usuario`:
```python
@dataclass
class Usuario:
    nombre: str
    contrasena: str
    rol: str  # "mesero", "chef", "gerente"
    
    def verificar_contrasena(self, contrasena):
        # En producción, usar hashing
        return self.contrasena == contrasena
```

2. Crea ventana de login antes de `AplicacionRestaurante`
3. Modifica `AplicacionRestaurante` para recibir usuario
4. Restringe funciones según rol

### Ejercicio 4.2: Integración con Base de Datos SQL
**Objetivo:** Migrar de archivo TXT a SQLite

**Pasos:**

1. Usa `sqlite3`:
```python
import sqlite3

class BaseDatosSQLite:
    def __init__(self, db_name="restaurante.db"):
        self.conn = sqlite3.connect(db_name)
        self.crear_tablas()
    
    def crear_tablas(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ordenes (
                id INTEGER PRIMARY KEY,
                mesa INTEGER,
                comensales INTEGER,
                items TEXT,
                total REAL,
                fecha TEXT
            )
        """)
        self.conn.commit()
    
    def guardar_orden(self, orden):
        self.conn.execute("""
            INSERT INTO ordenes VALUES (?, ?, ?, ?, ?, ?)
        """, (orden.id_orden, orden.mesa, orden.comensales, 
              ";".join([f"{i[0].nombre}x{i[1]}" for i in orden.items]),
              orden.total, orden.fecha))
        self.conn.commit()
```

2. Reemplaza `BaseDatos` por `BaseDatosSQLite`

### Ejercicio 4.3: API REST con Flask
**Objetivo:** Crear API para acceder a datos remotamente

**Pasos:**

1. Instala Flask:
```bash
pip install flask flask-cors
```

2. Crea `api_restaurante.py`:
```python
from flask import Flask, jsonify, request
from restaurante_app import BaseDatos, Orden

app = Flask(__name__)

db = BaseDatos()

@app.route('/ordenes', methods=['GET'])
def obtener_ordenes():
    return jsonify({"ordenes": db.obtener_ordenes()})

@app.route('/ordenes/<id>', methods=['GET'])
def obtener_orden(id):
    ordenes = db.obtener_ordenes()
    for orden in ordenes:
        if orden.startswith(f"{id}|"):
            return jsonify({"orden": orden})
    return jsonify({"error": "No encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

3. Ejecuta con `python api_restaurante.py`
4. Accede a `http://localhost:5000/ordenes`

### Ejercicio 4.4: Panel de Administración Avanzado
**Objetivo:** Dashboard con estadísticas y gráficos

**Pasos:**

1. Instala Matplotlib:
```bash
pip install matplotlib
```

2. Crea método de análisis en `BaseDatos`:
```python
def obtener_estadisticas(self):
    ordenes = self.obtener_ordenes()
    total_ingresos = sum([float(o.split("|")[4]) for o in ordenes])
    total_ordenes = len(ordenes)
    promedio_por_orden = total_ingresos / total_ordenes if total_ordenes > 0 else 0
    
    return {
        "total_ordenes": total_ordenes,
        "total_ingresos": total_ingresos,
        "promedio_por_orden": promedio_por_orden
    }
```

3. Crea ventana de gráficos con Matplotlib

---

## 🏆 Proyecto Final Integrador

**Objetivo:** Combinar todos los ejercicios en una versión mejorada

**Requisitos:**
- ✅ Cambios de colores personalizados
- ✅ Búsqueda de productos funcional
- ✅ Sistema de descuentos
- ✅ Base de datos mejorada
- ✅ Exportación de datos
- ✅ Panel de estadísticas

**Entrega:**
1. Copia tu código a `restaurante_app_mejorado.py`
2. Documenta los cambios en `CAMBIOS.md`
3. Prueba todas las funciones
4. Compartir con otros estudiantes

---

## 📚 Recursos Adicionales

### Documentación
- Tkinter: https://docs.python.org/3/library/tkinter.html
- Python dataclasses: https://docs.python.org/3/library/dataclasses.html
- SQLite: https://docs.python.org/3/library/sqlite3.html
- Flask: https://flask.palletsprojects.com/

### Tutoriales
- Real Python - Tkinter: https://realpython.com/python-gui-tkinter/
- Tkinter Official: https://tcl.tk/

### Colores Útiles
- Color Palette: https://colorhunt.co/
- Hex Color Picker: https://www.w3schools.com/colors/colors_picker.asp

---

**¡Éxito en tus ejercicios!** 🎉

