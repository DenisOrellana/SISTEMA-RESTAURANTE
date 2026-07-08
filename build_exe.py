#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de construccion del ejecutable .exe - Sistema de Restaurante
Uso:   python build_exe.py
Salida: dist/SistemaRestaurante.exe
"""

import os
import sys
import subprocess
from pathlib import Path


def activar_entorno_virtual_local() -> None:
    """Reinicia el script usando el Python local de .venv si existe."""
    base_dir = Path(__file__).parent.resolve()
    if os.name == "nt":
        venv_python = base_dir / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = base_dir / ".venv" / "bin" / "python"

    if venv_python.exists():
        actual_python = Path(sys.executable).resolve()
        if actual_python != venv_python.resolve():
            print("[INFO] Se detectó un entorno virtual local .venv.")
            print("[INFO] Reiniciando con el Python de .venv...")
            # Usar subprocess.run con la ruta absoluta al script evita problemas
            # cuando la carpeta del proyecto contiene espacios en el nombre.
            script_path = str(Path(__file__).resolve())
            result = subprocess.run([str(venv_python), script_path] + sys.argv[1:])
            # Reenviar el código de salida del proceso hijo
            sys.exit(result.returncode)


activar_entorno_virtual_local()

# ─────────────────────────────────────────
# CONFIGURACION
# ─────────────────────────────────────────
NOMBRE_APP     = "SistemaRestaurante"
SCRIPT_ENTRADA = "ejecutar.py"
ICONO_ICO      = "icono_restaurante.ico"
CARPETA_SALIDA = "dist"


def instalar_pyinstaller() -> bool:
    """Instala PyInstaller si no esta disponible."""
    try:
        from PyInstaller import __version__ as pyinstaller_version
        print(f"[OK] PyInstaller {pyinstaller_version} listo.")
        return True
    except ImportError:
        print("[*] Instalando PyInstaller...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("[OK] PyInstaller instalado.")
            return True
        print(f"[ERROR] {result.stderr}")
        return False


def construir_exe(ico_path: str) -> bool:
    """Ejecuta PyInstaller para generar el .exe."""
    base_dir = Path(__file__).parent.resolve()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",                              # Un solo .exe
        "--windowed",                             # Sin consola negra
        f"--name={NOMBRE_APP}",
        f"--icon={ico_path}",
        f"--distpath={CARPETA_SALIDA}",
        "--add-data=restaurante_db.txt;.",
        "--add-data=icono_restaurante.svg;.",
        "--add-data=icono_restaurante.ico;.",
        "--add-data=icono_restaurante.png;.",
        SCRIPT_ENTRADA,
    ]

    print("\n[*] Ejecutando PyInstaller...")
    print("-" * 60)
    result = subprocess.run(cmd, cwd=str(base_dir))

    if result.returncode == 0:
        exe = base_dir / CARPETA_SALIDA / f"{NOMBRE_APP}.exe"
        print("\n" + "=" * 60)
        print("[OK] EXITO - Ejecutable listo:")
        print(f"     {exe}")
        print("=" * 60)
        return True
    else:
        print(f"[ERROR] PyInstaller fallo (codigo {result.returncode})")
        return False


def main():
    print("=" * 60)
    print("  SISTEMA RESTAURANTE  -  Generador de .EXE")
    print("=" * 60)

    base_dir = Path(__file__).parent.resolve()
    os.chdir(base_dir)

    # 1. Verificar script de entrada
    if not Path(SCRIPT_ENTRADA).exists():
        print(f"[ERROR] No se encontro: {SCRIPT_ENTRADA}")
        sys.exit(1)
    print(f"[OK] Script de entrada: {SCRIPT_ENTRADA}")

    # 2. Generar el icono con Pillow (SVG -> ICO via generar_icono.py)
    print("\n[1/2] Generando icono...")
    if not Path("generar_icono.py").exists():
        print("[ERROR] No se encontro generar_icono.py")
        sys.exit(1)

    result = subprocess.run([sys.executable, "generar_icono.py"], cwd=str(base_dir))
    if result.returncode != 0 or not Path(ICONO_ICO).exists():
        print("[ERROR] No se pudo generar el icono.")
        sys.exit(1)

    ico_path = str(base_dir / ICONO_ICO)

    # 3. Instalar / verificar PyInstaller
    print("\n[2/2] Verificando PyInstaller...")
    if not instalar_pyinstaller():
        sys.exit(1)

    # 4. Build del .exe
    if not construir_exe(ico_path):
        sys.exit(1)

    print("\n>> Para abrir la aplicacion, ejecuta:")
    print(f"   dist\\{NOMBRE_APP}.exe\n")


if __name__ == "__main__":
    main()
