import tkinter as tk

from restaurante_app import Producto, VistaPreviaOrden


def test_quitar_producto_desde_catalogo():
    root = tk.Tk()
    root.withdraw()

    try:
        vista = VistaPreviaOrden(root, lambda *args: None)
        producto = Producto(
            id=999,
            nombre="Prueba",
            descripcion="Producto de prueba",
            precio=10.5,
            categoria="Platillo",
            receta={},
        )

        vista.agregar_producto(producto)
        vista.quitar_producto(producto)

        assert vista.items_orden == {}
        assert vista.total == 0.0
    finally:
        root.destroy()
