# build/Gestion.spec
# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

ROOT = Path(SPECPATH).resolve().parent

APP = ROOT / 'app'

EXCLUDED_DIRS = {'tests', '__pycache__'}
EXCLUDED_SUFFIXES = {'.pyc', '.pyo'}

hiddenimports = (
    ['pymysql']
    + collect_submodules('sqlalchemy.dialects.mysql')
    + collect_submodules('app', filter=lambda n: 'tests' not in n.split('.'))
    + collect_submodules('zeroconf')
)

def collect_app_files():
    datas = []
    for path in APP.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(APP)
        # skip any file that lives under an excluded directory
        if any(part in EXCLUDED_DIRS for part in rel.parts[:-1]):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        datas.append((str(path), str(Path('app') / rel.parent)))
    return datas

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=collect_app_files(),  # Add relative paths for assets
    hookspath=[],
    hooksconfig={},
    hiddenimports=hiddenimports,
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
    name='Gestion',  # Exported executable name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for console-based apps
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../icon.ico'],  # Add relative path for the icon
)
