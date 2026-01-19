"""
CORE v4.0 - Build Script
Creates EXE with PyInstaller - WITH LOGO SUPPORT
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

APP_NAME = "CORE"
APP_VERSION = "4.0"
MAIN_SCRIPT = "main.py"
ICON_FILE = "CORE_LOGO.ico"
LOGO_FILE = "CORE_LOGO.png"

def clean_build():
    dirs_to_clean = ['build', 'dist', '__pycache__', '.pytest_cache']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}...")
            shutil.rmtree(dir_name)

    import glob
    for file in glob.glob('*.spec'):
        print(f"Removing {file}...")
        os.remove(file)

def create_ico_from_png():
    """PNG'den ICO oluştur (Pillow gerekli)"""
    try:
        from PIL import Image
        if os.path.exists(LOGO_FILE):
            img = Image.open(LOGO_FILE)
            # ICO için çoklu boyutlar
            icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
            img.save(ICON_FILE, format='ICO', sizes=icon_sizes)
            print(f"Created {ICON_FILE} from {LOGO_FILE}")
            return True
    except ImportError:
        print("Pillow not installed, skipping ICO creation")
    except Exception as e:
        print(f"Error creating ICO: {e}")
    return False

def create_spec_file():
    # Icon varsa ekle
    icon_line = ""
    if os.path.exists(ICON_FILE):
        icon_line = f"icon='{ICON_FILE}',"
    elif os.path.exists('icon.ico'):
        icon_line = "icon='icon.ico',"
    
    # Logo ve HTML dosyalarını data olarak ekle
    datas = [('index.html', '.')]
    if os.path.exists(LOGO_FILE):
        datas.append((LOGO_FILE, '.'))
    
    datas_str = str(datas)
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

hidden_imports = [
    'webview',
    'webview.platforms.winforms',
    'webview.platforms.edgechromium',
    'clr',
    'clr_loader',
    'pythonnet',
    'pandas',
    'pandas._libs',
    'pandas._libs.tslibs',
    'openpyxl',
    'openpyxl.cell',
    'bcrypt',
    'bcrypt._bcrypt',
    'sqlite3',
    'reportlab',
    'reportlab.lib',
    'reportlab.platypus',
    'xlrd',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas={datas_str},
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CORE',
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
    {icon_line}
)
'''
    with open('CORE.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("Created CORE.spec")

def build_exe():
    print("=" * 60)
    print(f"Building {APP_NAME} v{APP_VERSION}...")
    print("=" * 60)

    if not os.path.exists('index.html'):
        print("ERROR: index.html not found!")
        return False

    if not os.path.exists(MAIN_SCRIPT):
        print(f"ERROR: {MAIN_SCRIPT} not found!")
        return False
    
    # PNG'den ICO oluşturmayı dene
    if os.path.exists(LOGO_FILE) and not os.path.exists(ICON_FILE):
        create_ico_from_png()

    create_spec_file()

    cmd = [sys.executable, '-m', 'PyInstaller', '--clean', '--noconfirm', 'CORE.spec']
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("Build successful!")
        print(f"Executable: dist/{APP_NAME}.exe")
        return True
    print("Build failed!")
    return False

def build_folder():
    print("Building folder mode...")

    if not os.path.exists('index.html'):
        print("ERROR: index.html not found!")
        return False

    # PNG'den ICO oluşturmayı dene
    if os.path.exists(LOGO_FILE) and not os.path.exists(ICON_FILE):
        create_ico_from_png()

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', APP_NAME,
        '--windowed', '--noconfirm', '--clean',
        '--add-data', 'index.html;.',
        '--hidden-import', 'webview',
        '--hidden-import', 'webview.platforms.winforms',
        '--hidden-import', 'webview.platforms.edgechromium',
        '--hidden-import', 'pandas',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'bcrypt',
        '--hidden-import', 'clr',
        '--hidden-import', 'pythonnet',
        '--hidden-import', 'xlrd',
        MAIN_SCRIPT
    ]
    
    # Logo dosyasını ekle
    if os.path.exists(LOGO_FILE):
        cmd.extend(['--add-data', f'{LOGO_FILE};.'])

    # Icon varsa ekle
    if os.path.exists(ICON_FILE):
        cmd.extend(['--icon', ICON_FILE])
    elif os.path.exists('icon.ico'):
        cmd.extend(['--icon', 'icon.ico'])

    result = subprocess.run(cmd)
    return result.returncode == 0

def install_requirements():
    packages = ['pywebview', 'pythonnet', 'pandas', 'openpyxl', 'bcrypt', 'reportlab', 'pyinstaller', 'pillow', 'xlrd']
    for pkg in packages:
        print(f"Installing {pkg}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', pkg])

def main():
    if len(sys.argv) < 2:
        print("Usage: python build.py <command>")
        print("Commands: clean, install, exe, folder, ico, all")
        print("")
        print("  clean   - Remove build artifacts")
        print("  install - Install required packages")
        print("  exe     - Build single EXE file")
        print("  folder  - Build folder mode")
        print("  ico     - Create ICO from PNG")
        print("  all     - Clean and build EXE")
        return

    cmd = sys.argv[1].lower()

    if cmd == 'clean': clean_build()
    elif cmd == 'install': install_requirements()
    elif cmd == 'exe': clean_build(); build_exe()
    elif cmd == 'folder': clean_build(); build_folder()
    elif cmd == 'ico': create_ico_from_png()
    elif cmd == 'all': clean_build(); build_exe()
    else: print(f"Unknown: {cmd}")

if __name__ == "__main__":
    main()
