"""
CORE v4.0 - cx_Freeze Build Script
"""
import sys
from cx_Freeze import setup, Executable

# Build options
build_exe_options = {
    "packages": [
        "webview",
        "pandas",
        "openpyxl",
        "bcrypt",
        "sqlite3",
        "json",
        "pathlib",
        "datetime",
        "re",
        "os",
        "sys",
        "hashlib",
        "secrets",
    ],
    "includes": [
        "webview.platforms.winforms",
        "webview.platforms.edgechromium",
    ],
    "excludes": ["tkinter", "matplotlib", "scipy", "numpy.random._examples"],
    "include_files": [
        ("index.html", "index.html"),
        ("CORE_LOGO.png", "CORE_LOGO.png"),
    ],
    "optimize": 2,
}

# Base for Windows GUI application
base = "Win32GUI" if sys.platform == "win32" else None

# Executable
executables = [
    Executable(
        "main.py",
        base=base,
        target_name="CORE.exe",
        icon="CORE_LOGO.ico" if sys.platform == "win32" else None,
    )
]

setup(
    name="CORE",
    version="4.0",
    description="Cut Optimization & Reporting Engine",
    options={"build_exe": build_exe_options},
    executables=executables,
)
