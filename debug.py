#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de test verbose para diagnosticar errores"""

import sys
import traceback
import tkinter as tk

print("=" * 60)
print("DIAGNÓSTICO DE APLICACIÓN - Sistema de Gestión Restaurante")
print("=" * 60)

print("\n[1/4] Importando módulos...")
try:
    from restaurante_app import AplicacionRestaurante, Colores
    print("      ✓ Módulos importados exitosamente")
except Exception as e:
    print(f"      ✗ ERROR en importación: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[2/4] Creando ventana raíz...")
try:
    root = tk.Tk()
    root.geometry("1400x800")
    root.attributes('-topmost', True)
    print("      ✓ Ventana raíz creada")
except Exception as e:
    print(f"      ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[3/4] Inicializando AplicacionRestaurante...")
try:
    app = AplicacionRestaurante(root)
    print("      ✓ Aplicación inicializada correctamente")
except Exception as e:
    print(f"      ✗ ERROR en inicialización: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[4/4] Iniciando mainloop...")
try:
    # Traer ventana al frente
    root.after(100, lambda: root.attributes('-topmost', False))
    print("      ✓ Mainloop iniciado")
    print("\n" + "=" * 60)
    print("LA VENTANA DEBE ESTAR VISIBLE EN TU PANTALLA")
    print("=" * 60 + "\n")
    root.mainloop()
except Exception as e:
    print(f"      ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Programa finalizado normalmente")
