#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de diagnóstico para analizar anchos y espacios"""

import sys
import tkinter as tk
from tkinter import ttk

print("Iniciando diagnóstico del Canvas...")

try:
    from restaurante_app import AplicacionRestaurante, Colores
    
    root = tk.Tk()
    root.geometry("1400x800")
    root.attributes('-topmost', True)
    
    app = AplicacionRestaurante(root)
    
    # Esperar a que se dibuje la ventana
    root.update()
    
    # Obtener información de anchos
    print("\n[INFORMACIÓN DE ANCHOS]")
    print(f"Ancho total de ventana: {root.winfo_width()}px")
    print(f"Ancho de content_container: {app.content_container.winfo_width()}px")
    print(f"Ancho de catalogo.frame: {app.catalogo.frame.winfo_width()}px")
    
    # Intentar acceder al notebook
    if hasattr(app.catalogo, 'notebook'):
        print(f"Ancho de notebook: {app.catalogo.notebook.winfo_width()}px")
    
    print("\n✓ Dimensiones capturadas. Cerrando en 2 segundos...")
    root.after(2000, root.quit)
    root.mainloop()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
