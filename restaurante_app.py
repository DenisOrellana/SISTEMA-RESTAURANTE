"""
Sistema de Gestión de Restaurante - Interfaz Tkinter
Autor: Sistema de Gestión Restaurante
Tecnología: Python 3.x + Tkinter + TTK
Descripción: Aplicación completa de gestión de restaurante con GUI moderna
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from PIL import Image, ImageTk
import os


# ==================== CONFIGURACIÓN DE COLORES ====================
class Colores:
    """Paleta de colores del sistema (Pastel Rosa y Morado)"""
    FONDO_PRINCIPAL = "#F3EBF6"      # Lavanda/Morado muy claro y suave
    FONDO_TARJETAS = "#FFFFFF"       # Blanco puro
    ACENTO_NARANJA = "#C3AED6"       # Morado pastel suave (Mesa seleccionada / Encabezados)
    ACENTO_NARJANJA = "#C3AED6"      # Alias con el error de escritura solicitado para compatibilidad
    NARANJA_CLARO = "#D9CBF2"        # Morado pastel muy claro (Hover)
    NARANJA_OSCURO = "#A288BA"       # Morado un poco más intenso (Active/Presionado)
    TEXTO_OSCURO = "#3D3443"         # Gris oscuro con un toque de morado para el texto
    BORDE_GRIS = "#E5DDE9"           # Gris lila muy tenue para los bordes
    BLANCO = "#FFFFFF"               
    GRIS_INACTIVO = "#D2C9D6"        # Morado grisáceo apagado para botones inactivos


# ==================== CLASES DE DATOS ====================
@dataclass
class Producto:
    """Estructura de datos para un producto"""
    id: int
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    imagen: str = "imagenes/default.jpg"
    receta: dict = None
    
    def __post_init__(self):
        self.cantidad = 0
        if self.receta is None:
            self.receta = {}


@dataclass
class InventarioItem:
    """Estructura de datos para un ingrediente del inventario"""
    id: int
    nombre: str
    unidad: str
    cantidad: float
    minimo: float
    proveedor: str

    @property
    def estado(self):
        return "Bajo" if self.cantidad <= self.minimo else "Disponible"

    @property
    def indicador(self):
        return "⚠️ Bajo" if self.cantidad <= self.minimo else "✅ Disponible"

    def restock(self, cantidad):
        self.cantidad += cantidad


class Inventario:
    """Gestiona los ingredientes disponibles y el control de stock"""
    
    RUTA_INVENTARIO = "inventario_guardado.json"

    def __init__(self):
        self.items = self._cargar_inicial()

    def _cargar_inicial(self):
        """Carga el inventario desde archivo guardado o desde valores iniciales"""
        # Intentar cargar desde archivo
        items_cargados = self.cargar_inventario()
        if items_cargados:
            return items_cargados
        
        # Si no existe archivo, retornar valores iniciales
        return [
            InventarioItem(1, "Pollo", "kg", 20.0, 5.0, "Proveedor Carnes del Valle"),
            InventarioItem(2, "Carne", "kg", 12.0, 4.0, "Proveedor Carnes del Valle"),
            InventarioItem(3, "Camaron", "kg", 10.0, 3.0, "Proveedor Mar Fresco"),
            InventarioItem(4, "Queso", "kg", 8.0, 2.0, "Proveedor Lácteos La Granja"),
            InventarioItem(5, "Pasta", "kg", 10.0, 2.0, "Proveedor Pastas Delicias"),
            InventarioItem(6, "Crema", "L", 8.0, 2.0, "Proveedor Lácteos La Granja"),
            InventarioItem(7, "Salmon", "kg", 5.0, 1.5, "Proveedor Mar Fresco"),
            InventarioItem(8, "Chocolate", "kg", 4.0, 1.0, "Proveedor Dulces"),
            InventarioItem(9, "Harina", "kg", 6.0, 2.0, "Proveedor Harinas"),
            InventarioItem(10, "Leche", "L", 10.0, 3.0, "Proveedor Lácteos La Granja"),
            InventarioItem(11, "Azucar", "kg", 6.0, 1.5, "Proveedor Dulces"),
            InventarioItem(12, "Frutos Rojos", "kg", 3.0, 0.5, "Proveedor Frutas"),
            InventarioItem(13, "Agua", "uds", 50.0, 10.0, "Proveedor Bebidas"),
            InventarioItem(14, "Refrescos", "uds", 50.0, 10.0, "Proveedor Bebidas"),
            InventarioItem(15, "Frutas", "kg", 20.0, 5.0, "Proveedor Frutas"),
            InventarioItem(16, "Vino", "botellas", 12.0, 4.0, "Proveedor Vinoteca"),
            InventarioItem(17, "Cerveza", "botellas", 30.0, 8.0, "Proveedor Cervecería"),
            InventarioItem(18, "Mantequilla", "kg", 5.0, 1.0, "Proveedor Lácteos La Granja"),
        ]

    def obtener_items(self):
        return self.items

    def buscar_item(self, nombre):
        for item in self.items:
            if item.nombre.lower() == nombre.lower():
                return item
        return None

    def decrementar_por_receta(self, receta):
        if not receta:
            return
        # Validar primero la disponibilidad
        for nombre, cantidad in receta.items():
            ingrediente = self.buscar_item(nombre)
            if ingrediente is None:
                raise ValueError(f"Ingrediente '{nombre}' no está registrado en inventario")
            if ingrediente.cantidad < cantidad:
                raise ValueError(f"Stock insuficiente de {nombre}: {ingrediente.cantidad} {ingrediente.unidad}")
        # Descontar después de validar todo
        for nombre, cantidad in receta.items():
            ingrediente = self.buscar_item(nombre)
            ingrediente.cantidad -= cantidad

    def restock_item(self, nombre, cantidad):
        ingrediente = self.buscar_item(nombre)
        if ingrediente is None:
            raise ValueError(f"Ingrediente '{nombre}' no está registrado en inventario")
        ingrediente.restock(cantidad)

    def agregar_item(self, item):
        self.items.append(item)

    def guardar_inventario(self):
        """Guarda el estado actual del inventario en un archivo JSON"""
        try:
            datos = {
                "inventario": [
                    {
                        "id": item.id,
                        "nombre": item.nombre,
                        "unidad": item.unidad,
                        "cantidad": item.cantidad,
                        "minimo": item.minimo,
                        "proveedor": item.proveedor
                    }
                    for item in self.items
                ],
                "fecha_guardado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.RUTA_INVENTARIO, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar inventario: {e}")
            return False

    def cargar_inventario(self):
        """Carga el inventario desde el archivo JSON guardado"""
        try:
            ruta = Path(self.RUTA_INVENTARIO)
            if ruta.exists():
                with open(self.RUTA_INVENTARIO, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    items = []
                    for item_data in datos.get("inventario", []):
                        item = InventarioItem(
                            id=item_data["id"],
                            nombre=item_data["nombre"],
                            unidad=item_data["unidad"],
                            cantidad=item_data["cantidad"],
                            minimo=item_data["minimo"],
                            proveedor=item_data["proveedor"]
                        )
                        items.append(item)
                    return items if items else None
            return None
        except Exception as e:
            print(f"Error al cargar inventario: {e}")
            return None


@dataclass
class Orden:
    """Estructura de datos para una orden"""
    id_orden: int
    mesa: int
    comensales: int
    items: list  # Lista de (producto, cantidad)
    total: float
    fecha: str
    
    def a_txt(self):
        """Convierte la orden al formato de archivo de texto"""
        items_str = ";".join([f"{item[0].nombre}x{item[1]}" for item in self.items])
        return f"{self.id_orden}|{self.mesa}|{self.comensales}|{items_str}|{self.total:.2f}"


# ==================== BASE DE DATOS ====================
class BaseDatos:
    """Gestiona la persistencia de datos"""
    
    def __init__(self, ruta_archivo="restaurante_db.txt"):
        self.ruta = Path(ruta_archivo)
        self.ruta.touch(exist_ok=True)  # Crear archivo si no existe
    
    def guardar_orden(self, orden: Orden):
        """Guarda una orden en el archivo"""
        try:
            with open(self.ruta, "a", encoding="utf-8") as f:
                f.write(orden.a_txt() + "\n")
            return True
        except Exception as e:
            print(f"Error al guardar orden: {e}")
            return False
    
    def obtener_ordenes(self):
        """Obtiene todas las órdenes del archivo"""
        ordenes = []
        try:
            if self.ruta.exists():
                with open(self.ruta, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if linea:
                            ordenes.append(linea)
        except Exception as e:
            print(f"Error al leer órdenes: {e}")
        return ordenes


# ==================== CATÁLOGO DE PRODUCTOS ====================
class CatalogoComienzo:
    """Define el catálogo de productos del restaurante"""
    
    @staticmethod
    def obtener_productos():
        """Retorna el catálogo completo de productos"""
        productos = {
            "PLATILLOS": {
                "Entradas": [
                    Producto(1, "Alitas Picantes", "Alitas crujientes con salsa picante casera", 8.99, "Entradas", "imagenes/alitas.jpg", receta={"Pollo": 0.35, "Queso": 0.02}),
                    Producto(2, "Camarones Empanizados", "Camarones frescos empanizados al horno", 12.50, "Entradas", "imagenes/camarones.jpg", receta={"Camaron": 0.25, "Harina": 0.08}),
                    Producto(3, "Tabla de Quesos", "Selección de quesos artesanales importados", 14.99, "Entradas", "imagenes/tabla quesos.jpg", receta={"Queso": 0.25}),
                ],
                "Fuerte": [
                    Producto(4, "Filete Mignon", "Filete de res de 250g con champiñones", 24.99, "Fuerte", "imagenes/filete mignon.jpg", receta={"Carne": 0.4, "Queso": 0.04}),
                    Producto(5, "Pechuga Rellena", "Pechuga de pollo rellena de jamón y queso", 16.50, "Fuerte", "imagenes/pechuga rellena.jpg", receta={"Pollo": 0.3, "Queso": 0.05}),
                    Producto(6, "Pasta Alfredo", "Pasta fresca con salsa cremosa de champiñones", 14.99, "Fuerte", "imagenes/pasta alfredo.jpg", receta={"Pasta": 0.22, "Crema": 0.18, "Queso": 0.04}),
                    Producto(7, "Salmón a la Mantequilla", "Salmón fresco con salsa de vino blanco", 22.99, "Fuerte", "imagenes/Salmon a la mantequilla.jpg", receta={"Salmon": 0.28, "Mantequilla": 0.05}),
                ],
                "Postre": [
                    Producto(8, "Brownie de Chocolate", "Brownie casero con helado de vainilla", 7.99, "Postre", "imagenes/browni.jpg", receta={"Chocolate": 0.18, "Harina": 0.12, "Azucar": 0.05, "Leche": 0.05}),
                    Producto(9, "Flan Napolitano", "Flan casero con caramelo crujiente", 6.99, "Postre", "imagenes/napolitano.jpg", receta={"Leche": 0.25, "Azucar": 0.06, "Frutos Rojos": 0.05}),
                    Producto(10, "Cheesecake Clásico", "Cheesecake de Nueva York con frutos rojos", 9.50, "Postre", "imagenes/cheesecake.jpg", receta={"Queso": 0.22, "Azucar": 0.08, "Harina": 0.05}),
                ],
            },
            "BEBIDAS": {
                "Bebidas": [
                    Producto(11, "Agua Mineral", "Botella de agua mineral 500ml", 2.50, "Bebidas", "imagenes/agua mineral.jpg", receta={"Agua": 1.0}),
                    Producto(12, "Refresco", "Refresco surtido 330ml", 3.00, "Bebidas", "imagenes/refresco.jpg", receta={"Refrescos": 1.0}),
                    Producto(13, "Jugo Natural", "Jugo recién exprimido de frutas frescas", 5.99, "Bebidas", "imagenes/jugo natural.jpg", receta={"Frutas": 0.4, "Agua": 0.2}),
                    Producto(14, "Vino Tinto", "Vino tinto reserva 2019", 22.99, "Bebidas", "imagenes/vino.jpg", receta={"Vino": 1.0}),
                    Producto(15, "Cerveza Premium", "Cerveza artesanal local 355ml", 4.99, "Bebidas", "imagenes/cerveza.jpg", receta={"Cerveza": 1.0}),
                ],
            }
        }
        return productos


# ==================== INTERFAZ GRÁFICA ====================
class BarraLateral:
    """Componente de barra lateral de navegación"""
    
    def __init__(self, parent, on_select_callback):
        self.frame = tk.Frame(parent, bg=Colores.BLANCO, width=150)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.on_select = on_select_callback
        self.botones = {}
        self.botones_activos = {}
        
        self._crear_botones()
    
    def _crear_botones(self):
        """Crea los botones de navegación"""
        opciones = [
            ("Control de Mesas", "mesas"),
            ("Catálogo de Menú", "catalogo"),
            ("Control de Inventario", "inventario"),
            ("Confirmación de Orden", "confirmacion"),
            ("Historial y Control", "historial"),
            ("Configuración", "configuracion"),
            ("🚪 Salir Admin", "salir_admin"),
        ]
        
        # Logo/título
        titulo = tk.Label(
            self.frame,
            text="🍽️ RESTAURANTE",
            bg=Colores.BLANCO,
            fg=Colores.ACENTO_NARANJA,
            font=("Segoe UI", 11, "bold"),
            pady=20
        )
        titulo.pack(fill=tk.X, padx=10)
        
        # Separador
        sep = tk.Frame(self.frame, bg=Colores.BORDE_GRIS, height=1)
        sep.pack(fill=tk.X, pady=5)
        
        # Botones
        for nombre, codigo in opciones:
            btn = tk.Button(
                self.frame,
                text=nombre,
                bg=Colores.BLANCO,
                fg=Colores.TEXTO_OSCURO,
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                bd=0,
                padx=15,
                pady=15,
                anchor=tk.W,
                command=lambda c=codigo, n=nombre: self._activar_boton(c, n)
            )
            btn.pack(fill=tk.X, padx=0, pady=5)
            self.botones[codigo] = (btn, nombre)
            self.botones_activos[codigo] = False
            
            # Efectos hover
            btn.bind("<Enter>", lambda e, c=codigo: self._on_hover_enter(c))
            btn.bind("<Leave>", lambda e, c=codigo: self._on_hover_leave(c))
        
        # Activar botón de catálogo por defecto
        self._activar_boton("catalogo", "Catálogo de Menú")
    
    def _activar_boton(self, codigo, nombre):
        """Activa un botón y desactiva los demás"""
        for cod, (btn, _) in self.botones.items():
            if cod == codigo:
                btn.config(bg=Colores.NARANJA_CLARO, fg=Colores.ACENTO_NARANJA, font=("Segoe UI", 10, "bold"))
                self.botones_activos[cod] = True
            else:
                btn.config(bg=Colores.BLANCO, fg=Colores.TEXTO_OSCURO, font=("Segoe UI", 10))
                self.botones_activos[cod] = False
        
        self.on_select(codigo)
    
    def _on_hover_enter(self, codigo):
        """Efecto hover al entrar"""
        btn, _ = self.botones[codigo]
        if not self.botones_activos[codigo]:
            btn.config(bg=Colores.NARANJA_CLARO)
    
    def _on_hover_leave(self, codigo):
        """Efecto hover al salir"""
        btn, _ = self.botones[codigo]
        if not self.botones_activos[codigo]:
            btn.config(bg=Colores.BLANCO)


class TarjetaProducto:
    """Tarjeta visual de un producto"""
    
    def __init__(self, parent, producto, on_agregar_callback):
        self.producto = producto
        self.on_agregar = on_agregar_callback
        
        self.frame = tk.Frame(
            parent,
            bg=Colores.BLANCO,
            relief=tk.FLAT,
            bd=0,
            highlightbackground=Colores.BORDE_GRIS,
            highlightthickness=1
        )
        
        # Espacio para imagen del producto
        img_frame = tk.Frame(self.frame, bg=Colores.ACENTO_NARANJA, height=150)
        img_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        img_frame.pack_propagate(False)  # Mantener altura fija
        
        img_label = tk.Label(img_frame, bg=Colores.ACENTO_NARANJA)
        img_label.pack(expand=True)
        
        # Intentar cargar la imagen
        self.img_ref = None  # Referencia para mantener la imagen en memoria
        try:
            if os.path.exists(producto.imagen):
                img = Image.open(producto.imagen)
                img.thumbnail((220, 150), Image.Resampling.LANCZOS)
                self.img_ref = ImageTk.PhotoImage(img)
                img_label.config(image=self.img_ref)
            else:
                # Mostrar emoji si la imagen no existe
                img_label.config(
                    text="📷",
                    fg=Colores.BLANCO,
                    font=("Segoe UI", 30)
                )
        except Exception as e:
            # En caso de error, mostrar emoji
            print(f"Error cargando imagen {producto.imagen}: {e}")
            img_label.config(
                text="📷",
                fg=Colores.BLANCO,
                font=("Segoe UI", 30)
            )
        
        # Nombre del producto
        nombre_label = tk.Label(
            self.frame,
            text=producto.nombre,
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 10, "bold"),
            wraplength=220
        )
        nombre_label.pack(padx=10, pady=(5, 2), anchor=tk.W)
        
        # Descripción
        desc_label = tk.Label(
            self.frame,
            text=producto.descripcion,
            bg=Colores.BLANCO,
            fg=Colores.GRIS_INACTIVO,
            font=("Segoe UI", 8),
            wraplength=220,
            justify=tk.LEFT
        )
        desc_label.pack(padx=10, pady=(0, 8), anchor=tk.W)
        
        # Frame inferior: precio y botón
        footer_frame = tk.Frame(self.frame, bg=Colores.BLANCO)
        footer_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Precio
        precio_label = tk.Label(
            footer_frame,
            text=f"${producto.precio:.2f}",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=4,
            relief=tk.FLAT,
            bd=0
        )
        precio_label.pack(side=tk.LEFT)
        
        # Botón +
        self.btn_agregar = tk.Button(
            footer_frame,
            text="➕",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=2,
            command=self._agregar_producto
        )
        self.btn_agregar.pack(side=tk.RIGHT)
        
        # Eventos hover del botón
        self.btn_agregar.bind("<Enter>", self._on_btn_hover_enter)
        self.btn_agregar.bind("<Leave>", self._on_btn_hover_leave)
    
    def _agregar_producto(self):
        """Agrega el producto a la orden"""
        self.on_agregar(self.producto)
    
    def _on_btn_hover_enter(self, event):
        """Cambio de color al pasar el mouse"""
        self.btn_agregar.config(bg=Colores.NARANJA_OSCURO)
    
    def _on_btn_hover_leave(self, event):
        """Vuelve al color normal"""
        self.btn_agregar.config(bg=Colores.ACENTO_NARANJA)
    
    def pack(self, **kwargs):
        """Empaqueta el frame"""
        self.frame.pack(**kwargs)


class CatalogoMenu:
    """Sección del catálogo de menú"""
    
    def __init__(self, parent, on_agregar_callback):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        
        self.on_agregar = on_agregar_callback
        self.tarjetas = {}
        self.catalogo = CatalogoComienzo.obtener_productos()
        
        self._crear_interfaz()
    
    def get_frame(self):
        """Retorna el frame sin empaquetarlo"""
        return self.frame
    
    def _crear_interfaz(self):
        """Crea la interfaz del catálogo"""
        # Encabezado
        header = tk.Frame(self.frame, bg=Colores.ACENTO_NARANJA)
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="🍽️ Catálogo de Menú",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 14, "bold"),
            pady=15
        )
        titulo.pack()
        
        # Contenedor con pestañas
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Personalizar estilo de pestañas
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=Colores.FONDO_PRINCIPAL)
        style.configure('TNotebook.Tab', padding=[20, 10], font=("Segoe UI", 10))
        
        # Pestaña 1: Entradas
        tab_entradas = tk.Frame(self.notebook, bg=Colores.FONDO_PRINCIPAL)
        self.notebook.add(tab_entradas, text="ENTRADAS")
        self._crear_tab_categoria(tab_entradas, "Entradas", self.catalogo["PLATILLOS"]["Entradas"])
        
        # Pestaña 2: Platillos Fuertes
        tab_fuertes = tk.Frame(self.notebook, bg=Colores.FONDO_PRINCIPAL)
        self.notebook.add(tab_fuertes, text="PLATILLOS FUERTES")
        self._crear_tab_categoria(tab_fuertes, "Fuerte", self.catalogo["PLATILLOS"]["Fuerte"])
        
        # Pestaña 3: Postres
        tab_postres = tk.Frame(self.notebook, bg=Colores.FONDO_PRINCIPAL)
        self.notebook.add(tab_postres, text="POSTRES")
        self._crear_tab_categoria(tab_postres, "Postre", self.catalogo["PLATILLOS"]["Postre"])
        
        # Pestaña 4: Bebidas
        tab_bebidas = tk.Frame(self.notebook, bg=Colores.FONDO_PRINCIPAL)
        self.notebook.add(tab_bebidas, text="BEBIDAS")
        self._crear_tab_categoria(tab_bebidas, "Bebidas", self.catalogo["BEBIDAS"]["Bebidas"])

    def _crear_tab_categoria(self, parent_tab, categoria_key, productos_lista):
        # Canvas con scroll
        canvas = tk.Canvas(parent_tab, bg=Colores.FONDO_PRINCIPAL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent_tab, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Colores.FONDO_PRINCIPAL)
        
        # Crear ventana del canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Hacer que scrollable_frame se expanda al ancho del canvas
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Expandir frame al ancho del canvas
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:
                canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_frame_configure)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Contenedor de columnas
        contenedor = tk.Frame(scrollable_frame, bg=Colores.FONDO_PRINCIPAL)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Grid de 3 columnas
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        contenedor.columnconfigure(2, weight=1)
        
        for idx, producto in enumerate(productos_lista):
            row = idx // 3
            col = idx % 3
            frame_prod = tk.Frame(contenedor, bg=Colores.FONDO_PRINCIPAL)
            frame_prod.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
            tarjeta = TarjetaProducto(frame_prod, producto, self.on_agregar)
            tarjeta.pack(fill=tk.BOTH, expand=True)
            self.tarjetas[producto.id] = tarjeta





class VistaPreviaOrden:
    """Panel de vista previa de la orden actual"""
    
    def __init__(self, parent, on_confirmar_callback):
        self.frame = tk.Frame(
            parent,
            bg=Colores.BLANCO,
            relief=tk.FLAT,
            bd=0,
            highlightbackground=Colores.BORDE_GRIS,
            highlightthickness=1
        )
        # NO empaquetar aquí - se hará en _crear_secciones
        
        self.on_confirmar = on_confirmar_callback
        self.items_orden = {}  # {id_producto: {"producto": Producto, "cantidad": int}}
        self.total = 0.0
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de vista previa"""
        # Encabezado
        header = tk.Label(
            self.frame,
            text="📋 Orden Actual",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 11, "bold"),
            pady=10,
            relief=tk.FLAT,
            bd=0
        )
        header.pack(fill=tk.X)
        
        # Separador
        sep = tk.Frame(self.frame, bg=Colores.BORDE_GRIS, height=1)
        sep.pack(fill=tk.X)
        
        # Contenedor de items con scroll
        canvas_frame = tk.Frame(self.frame, bg=Colores.BLANCO)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg=Colores.BLANCO, highlightthickness=0, width=180)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.items_frame = tk.Frame(canvas, bg=Colores.BLANCO)
        
        self.items_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.items_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Etiqueta de items vacía
        self.label_vacio = tk.Label(
            self.items_frame,
            text="Sin artículos",
            bg=Colores.BLANCO,
            fg=Colores.GRIS_INACTIVO,
            font=("Segoe UI", 9, "italic")
        )
        self.label_vacio.pack(pady=20)
        
        # Separador
        sep2 = tk.Frame(self.frame, bg=Colores.BORDE_GRIS, height=1)
        sep2.pack(fill=tk.X)
        
        # Panel de totales
        totales_frame = tk.Frame(self.frame, bg=Colores.BLANCO)
        totales_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            totales_frame,
            text="Total:",
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 10, "bold")
        ).pack(side=tk.LEFT)
        
        self.label_total = tk.Label(
            totales_frame,
            text="$0.00",
            bg=Colores.BLANCO,
            fg=Colores.ACENTO_NARANJA,
            font=("Segoe UI", 11, "bold")
        )
        self.label_total.pack(side=tk.RIGHT)
        
        # Formulario de datos de mesa
        formulario_frame = tk.Frame(self.frame, bg=Colores.BLANCO)
        formulario_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(formulario_frame, text="Mesa:", bg=Colores.BLANCO, fg=Colores.TEXTO_OSCURO, font=("Segoe UI", 9)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_mesa = tk.Entry(formulario_frame, font=("Segoe UI", 9), width=10)
        self.entry_mesa.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.entry_mesa.config(state="readonly")
        
        tk.Label(formulario_frame, text="Comensales:", bg=Colores.BLANCO, fg=Colores.TEXTO_OSCURO, font=("Segoe UI", 9)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_comensales = tk.Entry(formulario_frame, font=("Segoe UI", 9), width=10)
        self.entry_comensales.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.entry_comensales.config(state="readonly")
        
        formulario_frame.columnconfigure(1, weight=1)
        
        # Botón Agregar Extra
        self.btn_extra = tk.Button(
            self.frame,
            text="➕ Agregar Extra",
            bg=Colores.GRIS_INACTIVO,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self._agregar_extra
        )
        self.btn_extra.pack(fill=tk.X, padx=10, pady=(5, 5))
        
        # Botón confirmar
        self.btn_confirmar = tk.Button(
            self.frame,
            text="✓ Confirmar Orden",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._confirmar_orden,
            state=tk.DISABLED
        )
        self.btn_confirmar.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Botón limpiar
        self.btn_limpiar = tk.Button(
            self.frame,
            text="🗑️ Limpiar",
            bg=Colores.BORDE_GRIS,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._limpiar_orden
        )
        self.btn_limpiar.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def establecer_mesa_comensales(self, mesa, comensales):
        """Establece los valores de mesa y comensales en modo lectura"""
        self.entry_mesa.config(state=tk.NORMAL)
        self.entry_comensales.config(state=tk.NORMAL)
        self.entry_mesa.delete(0, tk.END)
        self.entry_comensales.delete(0, tk.END)
        self.entry_mesa.insert(0, str(mesa))
        self.entry_comensales.insert(0, str(comensales))
        self.entry_mesa.config(state="readonly")
        self.entry_comensales.config(state="readonly")

    def _agregar_extra(self):
        """Abre un diálogo emergente para ingresar un artículo extra"""
        popup = tk.Toplevel(self.frame)
        popup.title("Agregar Artículo Extra")
        popup.geometry("300x200")
        popup.resizable(False, False)
        popup.config(bg=Colores.FONDO_PRINCIPAL)
        popup.transient(self.frame.winfo_toplevel())
        popup.grab_set()
        
        # Center popup
        popup.update_idletasks()
        x = self.frame.winfo_toplevel().winfo_rootx() + (self.frame.winfo_toplevel().winfo_width() // 2) - 150
        y = self.frame.winfo_toplevel().winfo_rooty() + (self.frame.winfo_toplevel().winfo_height() // 2) - 100
        popup.geometry(f"+{x}+{y}")
        
        tk.Label(popup, text="Nombre del Extra:", font=("Segoe UI", 9, "bold"), bg=Colores.FONDO_PRINCIPAL, fg=Colores.TEXTO_OSCURO).pack(pady=(15, 2))
        entry_nombre = tk.Entry(popup, font=("Segoe UI", 10), width=25)
        entry_nombre.pack(pady=2)
        entry_nombre.focus_set()
        
        tk.Label(popup, text="Precio ($):", font=("Segoe UI", 9, "bold"), bg=Colores.FONDO_PRINCIPAL, fg=Colores.TEXTO_OSCURO).pack(pady=(10, 2))
        entry_precio = tk.Entry(popup, font=("Segoe UI", 10), width=10, justify=tk.CENTER)
        entry_precio.pack(pady=2)
        entry_precio.insert(0, "0.00")
        
        def confirmar():
            nombre = entry_nombre.get().strip()
            precio_str = entry_precio.get().strip()
            if not nombre:
                messagebox.showerror("Error", "Ingrese el nombre del artículo extra", parent=popup)
                return
            try:
                precio = float(precio_str)
                if precio < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingrese un precio numérico válido mayor o igual a 0", parent=popup)
                return
                
            # Generar un ID único para el extra
            extra_id = 1000 + len(self.items_orden)
            prod_extra = Producto(
                id=extra_id,
                nombre=f"[Extra] {nombre}",
                descripcion="Artículo extra agregado manualmente",
                precio=precio,
                categoria="Extra",
                receta={}
            )
            self.agregar_producto(prod_extra)
            popup.destroy()
            
        btn_frame = tk.Frame(popup, bg=Colores.FONDO_PRINCIPAL)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Agregar", bg=Colores.ACENTO_NARANJA, fg=Colores.BLANCO, font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0, padx=10, pady=5, cursor="hand2", command=confirmar).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancelar", bg=Colores.GRIS_INACTIVO, fg=Colores.BLANCO, font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0, padx=10, pady=5, cursor="hand2", command=popup.destroy).pack(side=tk.RIGHT, padx=10)

    def agregar_producto(self, producto):
        """Agrega un producto a la orden"""
        # Eliminar etiqueta de vacío
        if self.label_vacio.winfo_exists():
            self.label_vacio.pack_forget()
        
        # Usar ID como clave, guardar producto y cantidad
        if producto.id in self.items_orden:
            self.items_orden[producto.id]["cantidad"] += 1
        else:
            self.items_orden[producto.id] = {"producto": producto, "cantidad": 1}
        
        self._actualizar_vista()
    
    def _actualizar_vista(self):
        """Actualiza la visualización de la orden"""
        # Limpiar items previos
        for widget in self.items_frame.winfo_children():
            if widget != self.label_vacio:
                widget.destroy()
        
        self.total = 0.0
        
        for id_producto, datos in self.items_orden.items():
            producto = datos["producto"]
            cantidad = datos["cantidad"]
            
            item_frame = tk.Frame(self.items_frame, bg=Colores.FONDO_PRINCIPAL)
            item_frame.pack(fill=tk.X, pady=5)
            
            # Nombre y cantidad
            info_label = tk.Label(
                item_frame,
                text=f"{producto.nombre} x{cantidad}",
                bg=Colores.FONDO_PRINCIPAL,
                fg=Colores.TEXTO_OSCURO,
                font=("Segoe UI", 9),
                anchor=tk.W,
                justify=tk.LEFT
            )
            info_label.pack(fill=tk.X)
            
            # Subtotal
            subtotal = producto.precio * cantidad
            self.total += subtotal
            
            subtotal_label = tk.Label(
                item_frame,
                text=f"${subtotal:.2f}",
                bg=Colores.FONDO_PRINCIPAL,
                fg=Colores.ACENTO_NARANJA,
                font=("Segoe UI", 9, "bold"),
                anchor=tk.E
            )
            subtotal_label.pack(fill=tk.X)
            
            # Botón eliminar
            btn_eliminar = tk.Button(
                item_frame,
                text="✕",
                bg=Colores.BLANCO,
                fg=Colores.ACENTO_NARANJA,
                font=("Segoe UI", 8),
                relief=tk.FLAT,
                bd=0,
                padx=5,
                command=lambda p_id=id_producto: self._eliminar_producto(p_id)
            )
            btn_eliminar.pack(pady=(5, 0))
        
        # Actualizar total
        self.label_total.config(text=f"${self.total:.2f}")
        
        # Activar/desactivar botón confirmar
        if self.items_orden:
            self.btn_confirmar.config(state=tk.NORMAL)
        else:
            self.btn_confirmar.config(state=tk.DISABLED)
            self.label_vacio.pack(pady=20)
    
    def _eliminar_producto(self, id_producto):
        """Elimina un producto de la orden"""
        if id_producto in self.items_orden:
            self.items_orden[id_producto]["cantidad"] -= 1
            if self.items_orden[id_producto]["cantidad"] <= 0:
                del self.items_orden[id_producto]
        self._actualizar_vista()
    
    def _confirmar_orden(self):
        """Confirma y guarda la orden"""
        try:
            mesa_str = self.entry_mesa.get()
            comensales_str = self.entry_comensales.get()
            if not mesa_str or not comensales_str:
                raise ValueError()
            mesa = int(mesa_str)
            comensales = int(comensales_str)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese mesa y comensales válidos")
            return
        
        if not self.items_orden:
            messagebox.showwarning("Advertencia", "La orden está vacía")
            return
        
        # Construir lista de items con producto y cantidad
        items_lista = []
        for id_producto, datos in self.items_orden.items():
            items_lista.append((datos["producto"], datos["cantidad"]))
        
        self.on_confirmar(mesa, comensales, items_lista, self.total)
    
    def _limpiar_orden(self):
        """Limpia la orden actual"""
        self.items_orden = {}  # Reinicializar diccionario
        self.entry_mesa.config(state=tk.NORMAL)
        self.entry_comensales.config(state=tk.NORMAL)
        self.entry_mesa.delete(0, tk.END)
        self.entry_comensales.delete(0, tk.END)
        self.entry_mesa.config(state="readonly")
        self.entry_comensales.config(state="readonly")
        self._actualizar_vista()


class ControlMesas:
    """Sección de control de mesas"""
    
    def __init__(self, parent, on_seleccionar_mesa):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        self.on_seleccionar_mesa = on_seleccionar_mesa
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de control de mesas"""
        # Encabezado
        header = tk.Frame(self.frame, bg=Colores.ACENTO_NARANJA)
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="🪑 Control de Mesas",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 14, "bold"),
            pady=15
        )
        titulo.pack()
        
        # Grid de mesas
        contenedor = tk.Frame(self.frame, bg=Colores.FONDO_PRINCIPAL)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for mesa in range(1, 17):  # 16 mesas
            btn = tk.Button(
                contenedor,
                text=f"Mesa {mesa}\n(Disponible)",
                bg=Colores.BLANCO,
                fg=Colores.TEXTO_OSCURO,
                font=("Segoe UI", 11, "bold"),
                relief=tk.RAISED,
                bd=1,
                width=15,
                height=5,
                cursor="hand2",
                command=lambda m=mesa: self._mesa_click(m)
            )
            btn.grid(row=(mesa-1)//4, column=(mesa-1)%4, padx=10, pady=10)

    def _mesa_click(self, mesa_num):
        """Maneja el clic en una mesa"""
        self.on_seleccionar_mesa(mesa_num)


class ConfirmacionOrden:
    """Sección de confirmación de órdenes"""
    
    def __init__(self, parent, db):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        self.db = db
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de confirmación"""
        # Encabezado
        header = tk.Frame(self.frame, bg=Colores.ACENTO_NARANJA)
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="✓ Confirmación de Orden",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 14, "bold"),
            pady=15
        )
        titulo.pack()
        
        # Contenedor
        contenedor = tk.Frame(self.frame, bg=Colores.FONDO_PRINCIPAL)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instrucción
        txt = tk.Label(
            contenedor,
            text="Las órdenes confirmadas aparecen aquí.\nSe guardan automáticamente en restaurante_db.txt",
            bg=Colores.FONDO_PRINCIPAL,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 10),
            justify=tk.CENTER
        )
        txt.pack(pady=20)
        
        # Área de texto para mostrar órdenes
        self.text_widget = scrolledtext.ScrolledText(
            contenedor,
            height=15,
            width=80,
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            font=("Courier New", 9),
            relief=tk.FLAT,
            bd=1,
            highlightbackground=Colores.BORDE_GRIS,
            highlightthickness=1
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botón refrescar
        btn_refrescar = tk.Button(
            contenedor,
            text="🔄 Refrescar",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._refrescar_ordenes
        )
        btn_refrescar.pack(pady=10)
        
        self._refrescar_ordenes()
    
    def _refrescar_ordenes(self):
        """Actualiza la lista de órdenes"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        
        ordenes = self.db.obtener_ordenes()
        if ordenes:
            header = "ID | MESA | COMENSALES | ITEMS | TOTAL\n"
            header += "-" * 80 + "\n"
            self.text_widget.insert(tk.END, header)
            for orden in ordenes:
                self.text_widget.insert(tk.END, orden + "\n")
        else:
            self.text_widget.insert(tk.END, "No hay órdenes registradas aún.")
        
        self.text_widget.config(state=tk.DISABLED)
    
    def agregar_orden_a_vista(self, texto_orden):
        """Agrega una nueva orden a la vista"""
        self._refrescar_ordenes()


class HistorialControl:
    """Sección de historial y control"""
    
    def __init__(self, parent, db):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        self.db = db
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de historial"""
        # Encabezado
        header = tk.Frame(self.frame, bg=Colores.ACENTO_NARANJA)
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="📊 Historial y Control",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 14, "bold"),
            pady=15
        )
        titulo.pack()
        
        # Contenedor
        contenedor = tk.Frame(self.frame, bg=Colores.FONDO_PRINCIPAL)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tabla de órdenes
        frame_tabla = tk.Frame(contenedor, bg=Colores.BLANCO)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview
        columns = ("ID", "Mesa", "Comensales", "Items", "Total")
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columns,
            height=15,
            show="headings"
        )
        
        # Definir columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._cargar_historial()
    
    def _cargar_historial(self):
        """Carga el historial de órdenes en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar órdenes
        ordenes = self.db.obtener_ordenes()
        for orden in ordenes:
            self.tree.insert("", tk.END, values=tuple(orden.split("|")))


class InventarioControl:
    """Sección de control de inventario"""

    def __init__(self, parent, app):
        self.app = app
        self.inventario = app.inventario
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        self._crear_interfaz()

    def _crear_interfaz(self):
        header = tk.Frame(self.frame, bg=Colores.ACENTO_NARANJA)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="📦 Control de Inventario",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 14, "bold"),
            pady=15
        )
        titulo.pack()

        contenedor = tk.Frame(self.frame, bg=Colores.FONDO_PRINCIPAL)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        info_text = tk.Label(
            contenedor,
            text="Gestiona ingredientes, stock disponible y alertas de bajo stock.",
            bg=Colores.FONDO_PRINCIPAL,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 10),
            justify=tk.LEFT
        )
        info_text.pack(fill=tk.X, pady=(0, 10))

        frame_tabla = tk.Frame(contenedor, bg=Colores.BLANCO, bd=1, relief=tk.FLAT)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Ingrediente", "Cantidad", "Unidad", "Mínimo", "Estado", "Proveedor")
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columns,
            show="headings",
            height=12
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor=tk.CENTER)
        self.tree.column("Ingrediente", width=160, anchor=tk.W)
        self.tree.column("Proveedor", width=140, anchor=tk.W)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        acciones_frame = tk.Frame(contenedor, bg=Colores.BLANCO)
        acciones_frame.pack(fill=tk.X, pady=15)

        tk.Label(
            acciones_frame,
            text="Ingrediente:",
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.entry_nombre = tk.Entry(acciones_frame, font=("Segoe UI", 10), width=20)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        tk.Label(
            acciones_frame,
            text="Cantidad:",
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 10)
        ).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)

        self.entry_cantidad = tk.Entry(acciones_frame, font=("Segoe UI", 10), width=10)
        self.entry_cantidad.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        btn_restock = tk.Button(
            acciones_frame,
            text="➕ Reponer",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            command=self._restock_item
        )
        btn_restock.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)

        btn_refrescar = tk.Button(
            acciones_frame,
            text="🔄 Refrescar",
            bg=Colores.NARANJA_OSCURO,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            command=self.actualizar_tabla
        )
        btn_refrescar.grid(row=0, column=5, sticky=tk.W, padx=5, pady=5)

        acciones_frame.columnconfigure(1, weight=1)
        acciones_frame.columnconfigure(3, weight=0)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for ingrediente in self.inventario.obtener_items():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    ingrediente.id,
                    ingrediente.nombre,
                    f"{ingrediente.cantidad:.2f}",
                    ingrediente.unidad,
                    f"{ingrediente.minimo:.2f}",
                    ingrediente.indicador,
                    ingrediente.proveedor
                )
            )

    def _restock_item(self):
        nombre = self.entry_nombre.get().strip()
        cantidad_text = self.entry_cantidad.get().strip()
        if not nombre or not cantidad_text:
            messagebox.showwarning("Advertencia", "Ingrese ingrediente y cantidad para reponer")
            return
        try:
            cantidad = float(cantidad_text)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return

        try:
            self.inventario.restock_item(nombre, cantidad)
            messagebox.showinfo("Inventario", f"Se repuso {cantidad:.2f} {nombre}")
            self.entry_nombre.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.actualizar_tabla()
        except ValueError as e:
            messagebox.showerror("Error", str(e))


class Configuracion:
    """Sección de configuración"""
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de configuración"""
        # Encabezado
        header = tk.Frame(self.frame, bg=Colores.ACENTO_NARANJA)
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="⚙️ Configuración",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 14, "bold"),
            pady=15
        )
        titulo.pack()
        
        # Contenedor
        contenedor = tk.Frame(self.frame, bg=Colores.FONDO_PRINCIPAL)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Información del sistema
        info_frame = tk.Frame(contenedor, bg=Colores.BLANCO, relief=tk.FLAT, bd=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            info_frame,
            text="📋 Información del Sistema",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 11, "bold"),
            pady=10
        ).pack(fill=tk.X)
        
        info_text = """
• Versión: 1.0.0
• Tipo de Base de Datos: Archivo de Texto (restaurante_db.txt)
• Formato: ID|Mesa|Comensales|Items|Total
• Estado: Operativo
• Última actualización: 2026-06-16
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            font=("Segoe UI", 9),
            justify=tk.LEFT,
            anchor=tk.W
        ).pack(fill=tk.BOTH, padx=15, pady=10)
        
        # Opciones de configuración
        opt_frame = tk.Frame(contenedor, bg=Colores.BLANCO, relief=tk.FLAT, bd=1)
        opt_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            opt_frame,
            text="🔧 Opciones",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 11, "bold"),
            pady=10
        ).pack(fill=tk.X)
        
        btn_export = tk.Button(
            opt_frame,
            text="📤 Exportar Datos",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_export.pack(pady=5, padx=15)
        
        btn_reset = tk.Button(
            opt_frame,
            text="🔄 Reiniciar Base de Datos",
            bg=Colores.NARANJA_OSCURO,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_reset.pack(pady=5, padx=15)
        
        btn_about = tk.Button(
            opt_frame,
            text="ℹ️  Acerca De",
            bg=Colores.GRIS_INACTIVO,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._mostrar_acerca
        )
        btn_about.pack(pady=(5, 15), padx=15)
    
    def _mostrar_acerca(self):
        """Muestra el diálogo Acerca De"""
        messagebox.showinfo(
            "Acerca De",
            "Sistema de Gestión de Restaurante\n"
            "Versión 1.0.0\n\n"
            "Desarrollado con Python 3.x y Tkinter\n"
            "Diseño: Interfaz moderna y plana (Flat Design)\n\n"
            "© 2026 - Todos los derechos reservados"
        )

# ==================== NUEVAS CLASES PARA EL FLUJO INTERACTIVO ====================

class DialogoComensales(tk.Toplevel):
    """Diálogo emergente moderno para ingresar la cantidad de comensales"""
    def __init__(self, parent, mesa_num, callback):
        super().__init__(parent)
        self.title(f"Mesa {mesa_num}")
        self.geometry("350x220")
        self.resizable(False, False)
        self.config(bg=Colores.FONDO_PRINCIPAL)
        self.transient(parent)
        self.grab_set()
        
        self.callback = callback
        self.mesa_num = mesa_num
        
        # Centrar el diálogo relativo al padre
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        # Elementos de Interfaz
        lbl_info = tk.Label(
            self,
            text=f"🍽️ Mesa {mesa_num}\nIngrese el número de comensales:",
            font=("Segoe UI", 11, "bold"),
            bg=Colores.FONDO_PRINCIPAL,
            fg=Colores.TEXTO_OSCURO,
            pady=15
        )
        lbl_info.pack()
        
        self.entry_comensales = tk.Entry(
            self,
            font=("Segoe UI", 12),
            justify=tk.CENTER,
            width=10,
            bd=1,
            relief=tk.SOLID
        )
        self.entry_comensales.pack(pady=5)
        self.entry_comensales.insert(0, "2")  # Por defecto 2 comensales
        self.entry_comensales.focus_set()
        self.entry_comensales.selection_range(0, tk.END)
        
        # Vincular la tecla Enter
        self.bind("<Return>", lambda e: self._confirmar())
        
        btn_frame = tk.Frame(self, bg=Colores.FONDO_PRINCIPAL)
        btn_frame.pack(pady=15)
        
        btn_aceptar = tk.Button(
            btn_frame,
            text="Aceptar",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            command=self._confirmar,
            cursor="hand2"
        )
        btn_aceptar.pack(side=tk.LEFT, padx=10)
        
        btn_cancelar = tk.Button(
            btn_frame,
            text="Cancelar",
            bg=Colores.GRIS_INACTIVO,
            fg=Colores.BLANCO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            command=self.destroy,
            cursor="hand2"
        )
        btn_cancelar.pack(side=tk.RIGHT, padx=10)
        
    def _confirmar(self):
        val = self.entry_comensales.get().strip()
        try:
            comensales = int(val)
            if comensales < 1 or comensales > 20:
                raise ValueError()
            self.callback(self.mesa_num, comensales)
            self.destroy()
        except ValueError:
            messagebox.showerror(
                "Error",
                "Por favor ingrese un número de comensales válido (entre 1 y 20)",
                parent=self
            )


class Portada:
    """Pantalla de inicio / portada del restaurante"""
    
    def __init__(self, parent, on_ingresar_callback, on_admin_callback):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        self.on_ingresar = on_ingresar_callback
        self.on_admin = on_admin_callback
        
        self._crear_interfaz()
        
    def _crear_interfaz(self):
        # Tarjeta contenedor centrada
        card = tk.Frame(
            self.frame,
            bg=Colores.BLANCO,
            relief=tk.FLAT,
            bd=0,
            highlightbackground=Colores.BORDE_GRIS,
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=520)
        
        # Logo o Emoji
        logo_label = tk.Label(card, bg=Colores.BLANCO)
        logo_label.pack(pady=(40, 10))
        
        # Intentar cargar icono_restaurante.png si existe
        self.img_ref = None
        if os.path.exists("icono_restaurante.png"):
            try:
                img = Image.open("icono_restaurante.png")
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                self.img_ref = ImageTk.PhotoImage(img)
                logo_label.config(image=self.img_ref)
            except Exception as e:
                print(f"Error cargando logo en portada: {e}")
                logo_label.config(text="🍽️", font=("Segoe UI", 60), fg=Colores.ACENTO_NARANJA)
        else:
            logo_label.config(text="🍽️", font=("Segoe UI", 60), fg=Colores.ACENTO_NARANJA)
            
        titulo = tk.Label(
            card,
            text="SISTEMA RESTAURANTE",
            font=("Segoe UI", 16, "bold"),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO
        )
        titulo.pack(pady=5)
        
        subtitulo = tk.Label(
            card,
            text="Bienvenido, por favor ingrese sus datos para comenzar",
            font=("Segoe UI", 9, "italic"),
            bg=Colores.BLANCO,
            fg=Colores.GRIS_INACTIVO
        )
        subtitulo.pack(pady=(0, 20))
        
        # Formulario
        form_frame = tk.Frame(card, bg=Colores.BLANCO)
        form_frame.pack(fill=tk.X, padx=50)
        
        lbl_nombre = tk.Label(
            form_frame,
            text="Nombre del Comensal Principal:",
            font=("Segoe UI", 10, "bold"),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            anchor=tk.W
        )
        lbl_nombre.pack(fill=tk.X, pady=(10, 2))
        
        self.entry_nombre = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bd=1,
            relief=tk.SOLID
        )
        self.entry_nombre.pack(fill=tk.X, ipady=5, pady=(0, 10))
        
        lbl_apellido = tk.Label(
            form_frame,
            text="Apellido del Comensal Principal:",
            font=("Segoe UI", 10, "bold"),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            anchor=tk.W
        )
        lbl_apellido.pack(fill=tk.X, pady=(10, 2))
        
        self.entry_apellido = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bd=1,
            relief=tk.SOLID
        )
        self.entry_apellido.pack(fill=tk.X, ipady=5, pady=(0, 20))
        
        # Botón Ingresar
        btn_ingresar = tk.Button(
            card,
            text="Ingresar al Sistema",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._ingresar
        )
        btn_ingresar.pack(fill=tk.X, padx=50, ipady=8, pady=10)
        
        # Botón Admin (discreto en la parte inferior derecha)
        btn_admin = tk.Button(
            card,
            text="🔑 Acceso Admin",
            bg=Colores.BLANCO,
            fg=Colores.GRIS_INACTIVO,
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._admin_click
        )
        btn_admin.place(x=400, y=485)
        
    def _ingresar(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        
        if not nombre or not apellido:
            messagebox.showerror("Error", "Por favor ingrese su nombre y apellido")
            return
            
        self.on_ingresar(nombre, apellido)
        
    def _admin_click(self):
        self.on_admin()


class PantallaPago:
    """Pantalla para confirmación del pago y datos de facturación"""
    
    def __init__(self, parent, total, cliente_nombre, cliente_apellido, items_orden, on_cancelar_callback, on_pagar_callback):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        self.total = total
        self.cliente_nombre = cliente_nombre
        self.cliente_apellido = cliente_apellido
        self.items_orden = items_orden
        self.on_cancelar = on_cancelar_callback
        self.on_pagar = on_pagar_callback
        
        self.metodo_pago = tk.StringVar(value="Efectivo")
        
        self._crear_interfaz()
        
    def _crear_interfaz(self):
        # Card contenedor
        card = tk.Frame(
            self.frame,
            bg=Colores.BLANCO,
            relief=tk.FLAT,
            bd=0,
            highlightbackground=Colores.BORDE_GRIS,
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=600, height=580)
        
        # Encabezado de Pago
        header = tk.Label(
            card,
            text="💳 DETALLE DE PAGO Y FACTURACIÓN",
            font=("Segoe UI", 14, "bold"),
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Info del comensal principal
        info_cliente = tk.Label(
            card,
            text=f"Cliente Principal: {self.cliente_nombre} {self.cliente_apellido}",
            font=("Segoe UI", 11, "bold"),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            pady=10
        )
        info_cliente.pack()
        
        # Contenedor de Detalle de Items
        items_card = tk.Frame(card, bg=Colores.FONDO_PRINCIPAL, bd=1, relief=tk.SOLID)
        items_card.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        # Scroll para items si hay muchos
        canvas = tk.Canvas(items_card, bg=Colores.FONDO_PRINCIPAL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(items_card, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Colores.FONDO_PRINCIPAL)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insertar items en la vista
        for id_prod, datos in self.items_orden.items():
            prod = datos["producto"]
            cant = datos["cantidad"]
            sub = prod.precio * cant
            
            lbl_item = tk.Label(
                scrollable_frame,
                text=f"{prod.nombre} x{cant:<3}   ${sub:.2f}",
                font=("Courier New", 10),
                bg=Colores.FONDO_PRINCIPAL,
                fg=Colores.TEXTO_OSCURO,
                anchor=tk.W,
                justify=tk.LEFT,
                pady=2
            )
            lbl_item.pack(fill=tk.X, padx=10)
            
        # Total destacado
        lbl_total = tk.Label(
            card,
            text=f"Total Consumido: ${self.total:.2f}",
            font=("Segoe UI", 14, "bold"),
            bg=Colores.BLANCO,
            fg=Colores.ACENTO_NARANJA,
            pady=10
        )
        lbl_total.pack()
        
        # Formulario de Facturación
        form_frame = tk.Frame(card, bg=Colores.BLANCO)
        form_frame.pack(fill=tk.X, padx=40, pady=10)
        
        lbl_factura = tk.Label(
            form_frame,
            text="Nombre para Facturación:",
            font=("Segoe UI", 10, "bold"),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO
        )
        lbl_factura.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.entry_factura = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bd=1,
            relief=tk.SOLID,
            width=30
        )
        self.entry_factura.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        # Por defecto, el comensal principal
        self.entry_factura.insert(0, f"{self.cliente_nombre} {self.cliente_apellido}")
        
        # Método de Pago
        lbl_metodo = tk.Label(
            form_frame,
            text="Método de Pago:",
            font=("Segoe UI", 10, "bold"),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO
        )
        lbl_metodo.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        radio_frame = tk.Frame(form_frame, bg=Colores.BLANCO)
        radio_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        rb_efectivo = tk.Radiobutton(
            radio_frame,
            text="Efectivo",
            variable=self.metodo_pago,
            value="Efectivo",
            font=("Segoe UI", 9),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            activebackground=Colores.BLANCO,
            cursor="hand2"
        )
        rb_efectivo.pack(side=tk.LEFT, padx=5)
        
        rb_tarjeta = tk.Radiobutton(
            radio_frame,
            text="Tarjeta",
            variable=self.metodo_pago,
            value="Tarjeta",
            font=("Segoe UI", 9),
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            activebackground=Colores.BLANCO,
            cursor="hand2"
        )
        rb_tarjeta.pack(side=tk.LEFT, padx=5)
        
        # Botones de Acción
        btn_frame = tk.Frame(card, bg=Colores.BLANCO)
        btn_frame.pack(fill=tk.X, padx=40, pady=20)
        
        btn_pagar = tk.Button(
            btn_frame,
            text="Finalizar y Pagar",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self._pagar
        )
        btn_pagar.pack(side=tk.RIGHT, padx=5)
        
        btn_cancelar = tk.Button(
            btn_frame,
            text="Atrás (Modificar Pedido)",
            bg=Colores.GRIS_INACTIVO,
            fg=Colores.BLANCO,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.on_cancelar
        )
        btn_cancelar.pack(side=tk.LEFT, padx=5)
        
    def _pagar(self):
        nombre_fact = self.entry_factura.get().strip()
        if not nombre_fact:
            messagebox.showerror("Error", "Por favor ingrese el nombre para la facturación")
            return
            
        metodo = self.metodo_pago.get()
        self.on_pagar(nombre_fact, metodo)


class PantallaFactura:
    """Pantalla que simula una factura de restaurante y muestra el ticket final"""
    
    def __init__(self, parent, id_orden, total, cliente_nombre, cliente_apellido, facturado_a, metodo_pago, mesa, comensales, items_orden, on_inicio_callback):
        self.frame = tk.Frame(parent, bg=Colores.FONDO_PRINCIPAL)
        self.id_orden = id_orden
        self.total = total
        self.cliente_nombre = cliente_nombre
        self.cliente_apellido = cliente_apellido
        self.facturado_a = facturado_a
        self.metodo_pago = metodo_pago
        self.mesa = mesa
        self.comensales = comensales
        self.items_orden = items_orden
        self.on_inicio = on_inicio_callback
        
        self._crear_interfaz()
        
    def _crear_interfaz(self):
        # Card contenedor
        card = tk.Frame(
            self.frame,
            bg=Colores.BLANCO,
            relief=tk.FLAT,
            bd=0,
            highlightbackground=Colores.BORDE_GRIS,
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=650)
        
        # Encabezado
        header = tk.Label(
            card,
            text="🧾 FACTURA DE VENTA",
            font=("Segoe UI", 12, "bold"),
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Simulación de Ticket Físico
        ticket = tk.Frame(
            card,
            bg=Colores.BLANCO,
            bd=1,
            relief=tk.SOLID,
            highlightbackground=Colores.BORDE_GRIS
        )
        ticket.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)
        
        # Contenido del Ticket (ScrolledText o Labels con tipografía Courier)
        ticket_text = scrolledtext.ScrolledText(
            ticket,
            bg=Colores.BLANCO,
            fg=Colores.TEXTO_OSCURO,
            font=("Courier New", 9),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10
        )
        ticket_text.pack(fill=tk.BOTH, expand=True)
        
        # Generar texto de la factura
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines = []
        lines.append("="*46)
        lines.append("🍽️  RESTAURANTE DELICIAS GOURMET  🍽️")
        lines.append("        Calle Principal #123, Tegucigalpa")
        lines.append(f" Fecha: {fecha_actual}")
        lines.append(f" Factura No: #F-{self.id_orden:06d}")
        lines.append("-"*46)
        lines.append(f" Comensal Principal: {self.cliente_nombre} {self.cliente_apellido}")
        lines.append(f" Facturado a:        {self.facturado_a}")
        lines.append(f" Mesa: {self.mesa:<14} Comensales: {self.comensales}")
        lines.append("="*46)
        lines.append(f"{' Cant x Item':<28}{'Precio':<8}{'Total':>8}")
        lines.append("-"*46)
        
        for id_prod, datos in self.items_orden.items():
            prod = datos["producto"]
            cant = datos["cantidad"]
            sub = prod.precio * cant
            
            # Formatear línea del item
            item_desc = f" {cant}x {prod.nombre}"
            if len(item_desc) > 26:
                item_desc = item_desc[:23] + "..."
                
            lines.append(f"{item_desc:<28}${prod.precio:<7.2f}${sub:>7.2f}")
            
        lines.append("-"*46)
        lines.append(f"{' SUBTOTAL:':<36}${self.total:>7.2f}")
        lines.append(f"{' IMPUESTO (15% Incl.):':<36}${self.total*0.15:>7.2f}")
        lines.append(f"{' TOTAL A PAGAR:':<36}${self.total:>7.2f}")
        lines.append("="*46)
        lines.append(f" Método de Pago: {self.metodo_pago}")
        lines.append("\n          ¡GRACIAS POR SU PREFERENCIA!          ")
        lines.append("="*46)
        
        # Insertar en el widget
        ticket_text.insert(tk.END, "\n".join(lines))
        ticket_text.config(state=tk.DISABLED)
        
        # Botón Volver al Inicio
        btn_inicio = tk.Button(
            card,
            text="Nuevo Cliente / Volver al Inicio",
            bg=Colores.ACENTO_NARANJA,
            fg=Colores.BLANCO,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.on_inicio
        )
        btn_inicio.pack(fill=tk.X, padx=40, pady=(0, 20))


class AplicacionRestaurante:
    """Aplicación principal del sistema de restaurante"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Sistema de Gestión de Restaurante")
        self.root.geometry("1400x750")
        self.root.config(bg=Colores.FONDO_PRINCIPAL)
        
        # Establecer icono de la ventana
        try:
            if os.path.exists("icono_restaurante.ico"):
                self.root.iconbitmap("icono_restaurante.ico")
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el icono: {e}")
        
        # Base de datos
        self.db = BaseDatos("restaurante_db.txt")
        self.inventario = Inventario()
        
        # Estados del flujo interactivo
        self.cliente_nombre = ""
        self.cliente_apellido = ""
        self.mesa_seleccionada = None
        self.comensales_seleccionados = 0
        self.admin_mode = False
        
        # Contenedor principal
        self.main_container = tk.Frame(self.root, bg=Colores.FONDO_PRINCIPAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Inicializar secciones
        self.secciones = {}
        
        # Contenedor para las secciones (derecha del sidebar si está visible)
        self.content_container = tk.Frame(self.main_container, bg=Colores.FONDO_PRINCIPAL)
        self.content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear secciones
        self._crear_secciones()
        
        # Crear barra lateral (oculta por defecto en flujo cliente)
        self.sidebar = BarraLateral(self.main_container, self._on_nav_select)
        self.sidebar.frame.pack_forget()
        
        # Mostrar sección inicial (Portada)
        self._mostrar_seccion("portada")
    
    def _crear_secciones(self):
        """Crea todas las secciones de la aplicación"""
        # Portada
        self.secciones["portada"] = Portada(
            self.content_container,
            on_ingresar_callback=self._on_ingresar_portada,
            on_admin_callback=self._on_acceso_admin
        ).frame
        
        # Control de Mesas (con callback de selección)
        self.secciones["mesas"] = ControlMesas(
            self.content_container,
            on_seleccionar_mesa=self._on_seleccionar_mesa
        ).frame
        
        # Catálogo de menú (con vista previa de orden)
        frame_catalogo_container = tk.Frame(self.content_container, bg=Colores.FONDO_PRINCIPAL)
        self.catalogo = CatalogoMenu(frame_catalogo_container, self._agregar_a_orden)
        self.vista_previa = VistaPreviaOrden(frame_catalogo_container, self._confirmar_orden_flow)
        
        self.catalogo.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vista_previa.frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        self.secciones["catalogo"] = frame_catalogo_container
        
        # Secciones administrativas
        self.inventario_control = InventarioControl(self.content_container, self)
        self.secciones["inventario"] = self.inventario_control.frame
        self.secciones["confirmacion"] = ConfirmacionOrden(self.content_container, self.db).frame
        self.secciones["historial"] = HistorialControl(self.content_container, self.db).frame
        self.secciones["configuracion"] = Configuracion(self.content_container).frame

    def _on_nav_select(self, codigo_seccion):
        """Callback cuando se selecciona una opción de navegación en el sidebar"""
        if codigo_seccion == "salir_admin":
            self.admin_mode = False
            self.sidebar._activar_boton("catalogo", "Catálogo de Menú")
            self._mostrar_seccion("portada")
        else:
            self._mostrar_seccion(codigo_seccion)

    def _mostrar_seccion(self, codigo_seccion):
        """Muestra la sección seleccionada y administra el sidebar"""
        if hasattr(self, "sidebar") and self.sidebar:
            if self.admin_mode:
                # Asegurar que el sidebar esté visible en la parte izquierda
                self.sidebar.frame.pack(side=tk.LEFT, fill=tk.Y)
                self.content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            else:
                # Flujo cliente: ocultar sidebar
                self.sidebar.frame.pack_forget()
                self.content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
        for codigo, frame in self.secciones.items():
            if codigo == codigo_seccion:
                frame.pack(fill=tk.BOTH, expand=True)
            else:
                frame.pack_forget()
    
    def _on_ingresar_portada(self, nombre, apellido):
        """Maneja el ingreso desde la portada y pasa a la selección de mesas"""
        self.cliente_nombre = nombre
        self.cliente_apellido = apellido
        self.vista_previa._limpiar_orden()
        self._mostrar_seccion("mesas")
        
    def _on_acceso_admin(self):
        """Valida contraseña y activa el panel administrativo"""
        popup = tk.Toplevel(self.root)
        popup.title("Acceso Admin")
        popup.geometry("300x160")
        popup.resizable(False, False)
        popup.config(bg=Colores.FONDO_PRINCIPAL)
        popup.transient(self.root)
        popup.grab_set()
        
        popup.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - 80
        popup.geometry(f"+{x}+{y}")
        
        tk.Label(
            popup,
            text="Contraseña de Administrador:\n(Por defecto: 1234)",
            font=("Segoe UI", 9, "bold"),
            bg=Colores.FONDO_PRINCIPAL,
            fg=Colores.TEXTO_OSCURO
        ).pack(pady=15)
        
        entry_pass = tk.Entry(popup, font=("Segoe UI", 10), show="*", width=15, justify=tk.CENTER)
        entry_pass.pack(pady=2)
        entry_pass.focus_set()
        
        def comprobar():
            passwd = entry_pass.get().strip()
            if passwd == "1234" or passwd == "":
                self.admin_mode = True
                self._mostrar_seccion("historial")  # ir a historial en admin por defecto
                popup.destroy()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta", parent=popup)
                
        btn_frame = tk.Frame(popup, bg=Colores.FONDO_PRINCIPAL)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Aceptar", bg=Colores.ACENTO_NARANJA, fg=Colores.BLANCO, font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0, padx=10, pady=5, cursor="hand2", command=comprobar).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancelar", bg=Colores.GRIS_INACTIVO, fg=Colores.BLANCO, font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0, padx=10, pady=5, cursor="hand2", command=popup.destroy).pack(side=tk.RIGHT, padx=10)
        
    def _on_seleccionar_mesa(self, mesa_num):
        """Maneja el clic en una mesa y abre el diálogo de comensales"""
        if self.admin_mode:
            messagebox.showinfo("Información", f"Mesa {mesa_num} seleccionada. En modo administrativo no se procesan comensales.")
            return
            
        DialogoComensales(self.root, mesa_num, self._on_confirmar_mesa_comensales)
        
    def _on_confirmar_mesa_comensales(self, mesa_num, comensales_num):
        """Establece la mesa y comensales seleccionados, y avanza al menú"""
        self.mesa_seleccionada = mesa_num
        self.comensales_seleccionados = comensales_num
        self.vista_previa.establecer_mesa_comensales(mesa_num, comensales_num)
        self._mostrar_seccion("catalogo")
        
    def _agregar_a_orden(self, producto):
        """Agrega un producto a la vista previa de orden"""
        self.vista_previa.agregar_producto(producto)
        
    def _confirmar_orden_flow(self, mesa, comensales, items, total):
        """Abre la pantalla de pago y facturación"""
        self.current_order_items = items
        self.current_order_total = total
        
        if "pago" in self.secciones:
            self.secciones["pago"].pack_forget()
            
        self.pantalla_pago = PantallaPago(
            self.content_container,
            total,
            self.cliente_nombre,
            self.cliente_apellido,
            self.vista_previa.items_orden,
            on_cancelar_callback=lambda: self._mostrar_seccion("catalogo"),
            on_pagar_callback=self._procesar_pago
        )
        self.secciones["pago"] = self.pantalla_pago.frame
        self._mostrar_seccion("pago")
        
    def _procesar_pago(self, facturado_a, metodo_pago):
        """Procesa el pago, descuenta stock, guarda la orden en la BD y muestra la factura"""
        items_lista = self.current_order_items
        total = self.current_order_total
        mesa = self.mesa_seleccionada
        comensales = self.comensales_seleccionados
        
        try:
            # Descontar ingredientes del inventario por cada platillo vendido
            receta_total = {}
            for producto, cantidad in items_lista:
                for nombre, valor in producto.receta.items():
                    receta_total[nombre] = receta_total.get(nombre, 0) + valor * cantidad

            self.inventario.decrementar_por_receta(receta_total)
            
            # Guardar el inventario actualizado en archivo
            self.inventario.guardar_inventario()
            
        except ValueError as e:
            messagebox.showerror("Error de inventario", str(e))
            return

        # Generar ID de orden
        ordenes_existentes = self.db.obtener_ordenes()
        id_orden = len(ordenes_existentes) + 1
        
        # Crear orden
        orden = Orden(
            id_orden=id_orden,
            mesa=mesa,
            comensales=comensales,
            items=items_lista,
            total=total,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Guardar en BD
        if self.db.guardar_orden(orden):
            # Refrescar listados administrativos
            if "confirmacion" in self.secciones:
                self._actualizar_confirmacion()
            if hasattr(self, "inventario_control"):
                self.inventario_control.actualizar_tabla()
            if "historial" in self.secciones:
                # Recargar tabla de historial
                self.secciones["historial"] = HistorialControl(self.content_container, self.db).frame
                
            # Crear y mostrar Factura
            if "factura" in self.secciones:
                self.secciones["factura"].pack_forget()
                
            self.pantalla_factura = PantallaFactura(
                self.content_container,
                id_orden,
                total,
                self.cliente_nombre,
                self.cliente_apellido,
                facturado_a,
                metodo_pago,
                mesa,
                comensales,
                self.vista_previa.items_orden,
                on_inicio_callback=self._volver_al_inicio
            )
            self.secciones["factura"] = self.pantalla_factura.frame
            self._mostrar_seccion("factura")
        else:
            messagebox.showerror("Error", "No se pudo guardar la orden")
            
    def _volver_al_inicio(self):
        """Reinicia los datos de cliente y regresa a la portada"""
        self.cliente_nombre = ""
        self.cliente_apellido = ""
        self.mesa_seleccionada = None
        self.comensales_seleccionados = 0
        self.vista_previa._limpiar_orden()
        self._mostrar_seccion("portada")

    def _actualizar_confirmacion(self):
        pass


def main():
    """Función principal"""
    root = tk.Tk()
    app = AplicacionRestaurante(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Interrupción de teclado recibida. Cerrando la aplicación...")
        root.destroy()


if __name__ == "__main__":
    main()
