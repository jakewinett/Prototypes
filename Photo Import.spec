# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Import_Photos_macOS/import_photos_macos.py'],
    pathex=[],
    binaries=[],
    datas=[('Info.plist', '.')],
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
    [],
    exclude_binaries=True,
    name='Photo Import',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Photo Import',
)
app = BUNDLE(
    coll,
    name='Photo Import.app',
    icon=None,
    bundle_identifier='com.your-domain.photoimport',
)
