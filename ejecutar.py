#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Restaurante - Versión de Prueba Interactiva
"""

import os
import sys
import ctypes

# Establecer AppUserModelID ANTES de importar tkinter
# para que el icono del restaurante aparezca en la barra de tareas de Windows
try:
    myappid = 'sistemarestaurante.app.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

import tkinter as tk
from restaurante_app import AplicacionRestaurante

def main():
    """Función principal mejorada"""
    root = tk.Tk()
    
    # Configurar posición de ventana visible
    root.geometry("1400x800")
    root.attributes('-topmost', True)  # Mostrar ventana al frente
    
    try:
        app = AplicacionRestaurante(root)
        # Traer ventana al frente después de 100ms
        root.after(100, lambda: root.attributes('-topmost', False))
        root.mainloop()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
