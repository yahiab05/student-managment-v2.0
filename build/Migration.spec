from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


ROOT = Path(__name__).resolve().parent.parent


# Python modules that may be imported dynamically
hiddenimports = collect_submodules("mysql_wizard")


a = Analysis(
    [str(ROOT / "wizard.py")],
    pathex=[str(ROOT)],
    binaries=[],

    # Include the complete mysql_wizard directory:
    # mysql_wizard/ui/
    # mysql_wizard/sql/
    # etc.
    datas=[
        (
            str(ROOT / "mysql_wizard"),
            "mysql_wizard",
        ),
    ],

    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)


pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Migration Wizard",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)