#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de prueba para diagnosticar la aplicación"""

import sys
import traceback
import tkinter as tk

print("1. Importando restaurante_app...")
try:
    from restaurante_app import AplicacionRestaurante, Colores
    print("   ✓ Importación exitosa")
except Exception as e:
    print(f"   ✗ Error en importación: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n2. Creando ventana raíz...")
try:
    root = tk.Tk()
    print("   ✓ Ventana raíz creada")
except Exception as e:
    print(f"   ✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n3. Inicializando AplicacionRestaurante...")
try:
    app = AplicacionRestaurante(root)
    print("   ✓ Aplicación inicializada")
except Exception as e:
    print(f"   ✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n4. Configurando ventana...")
try:
    root.after(2000, root.quit)  # Cerrar después de 2 segundos
    print("   ✓ Temporizador configurado")
except Exception as e:
    print(f"   ✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n5. Iniciando mainloop...")
try:
    root.mainloop()
    print("   ✓ Mainloop completado")
except Exception as e:
    print(f"   ✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Prueba completada exitosamente!")
