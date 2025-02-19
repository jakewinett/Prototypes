# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['import_photos_macos.py'],
    pathex=['/Users/jakewinett/Desktop/Zibby/Prototypes/Import_Photos_macOS'],
    binaries=[],
    datas=[('Info.plist', '.')],
    hiddenimports=['PyQt6'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
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
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Photo Import'
)

app = BUNDLE(coll,
    name='Photo Import.app',
    icon=None,
    bundle_identifier='com.zibby.photoimport',
    info_plist={
        'NSPhotoLibraryUsageDescription': 'This app needs access to Photos to import your albums',
        'LSEnvironment': {'DYLD_LIBRARY_PATH': '@executable_path/../Frameworks'}
    },
)