# -*- mode: python ; coding: utf-8 -*-
import os
import glob
from pathlib import Path

block_cipher = None
HERE = Path.cwd()

# Discover all action modules for hidden imports
action_modules = []
for p in glob.glob(str(HERE / 'actions' / '*.py')):
    name = Path(p).stem
    if not name.startswith('__'):
        action_modules.append(f'actions.{name}')

# Discover core modules
core_modules = []
for p in glob.glob(str(HERE / 'core' / '*.py')):
    name = Path(p).stem
    if not name.startswith('__'):
        core_modules.append(f'core.{name}')

datas = [
    (str(HERE / 'core' / 'face_model.obj'), 'core'),
    (str(HERE / 'core' / 'prompt.txt'), 'core'),
    (str(HERE / 'Prompt.txt'), '.'),
    (str(HERE / 'ultron.jpeg'), '.'),
    (str(HERE / 'ultron_avatar.png'), '.'),
    (str(HERE / 'config' / 'jarvis.ico'), 'config'),
    (str(HERE / 'config' / 'api_keys.json.example'), 'config'),
    (str(HERE / 'dashboard' / 'static'), 'dashboard/static'),
    (str(HERE / 'actions'), 'actions'),
    (str(HERE / 'plugins'), 'plugins'),
    (str(HERE / 'memory' / 'workspace_presets.json'), 'memory'),
]

hiddenimports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.QtMultimedia',
    'sounddevice',
    'numpy',
    'miniaudio',
    'edge_tts',
    'pyttsx3',
    'speech_recognition',
    'psutil',
    'pyautogui',
    'pyperclip',
    'cv2',
    'mss',
    'fastapi',
    'uvicorn',
    'cryptography',
    'google.genai',
    'requests',
    'playwright',
    'comtypes',
    'pycaw',
    'win10toast',
    'wmi',
    'winrt',
    'bleak',
    'pynvml',
    'send2trash',
    'pptx',
    'docx',
    'pdfplumber',
    'pypdf',
    'openpyxl',
    'tinytuya',
    'paho.mqtt',
    'youtube_transcript_api',
    'pygetwindow',
    'pywinauto',
] + action_modules + core_modules

a = Analysis(
    ['main.py'],
    pathex=[str(HERE)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ZARVIS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(HERE / 'config' / 'jarvis.ico') if (HERE / 'config' / 'jarvis.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ZARVIS',
)
