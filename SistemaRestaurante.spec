# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ejecutar.py'],
    pathex=[],
    binaries=[],
    datas=[('restaurante_db.txt', '.'), ('icono_restaurante.svg', '.'), ('icono_restaurante.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SistemaRestaurante',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\denis\\Documents\\II PAC 2026\\SISTEMA RESTAURANTE\\icono_restaurante.ico'],
)
