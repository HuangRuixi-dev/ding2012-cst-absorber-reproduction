"""Load the locally installed CST 2023 libraries without global Python changes."""
from pathlib import Path
import os
import struct
import sys

_DLL_HANDLES = []


def bootstrap():
    if sys.version_info.major != 3 or sys.version_info.minor not in (6, 7, 8, 9) or struct.calcsize('P') != 8:
        raise RuntimeError('Use 64-bit Python 3.6-3.9 for the CST 2023 API.')
    root = Path(os.environ.get('CST_INSTALL_DIR', os.environ.get(
        'CST_INSTALLPATH_2023', r'D:\Program Files (x86)\CST Studio Suite 2023')))
    native = root / 'AMD64'
    libraries = native / 'python_cst_libraries'
    if not (libraries/'cst').is_dir():
        raise RuntimeError('Set CST_INSTALL_DIR to your licensed CST Studio Suite 2023 installation.')
    os.environ['CST_INSTALLPATH_2023'] = str(root)
    os.environ['PATH'] = str(native) + os.pathsep + os.environ.get('PATH', '')
    for path in (native, libraries):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    if hasattr(os, 'add_dll_directory'):
        _DLL_HANDLES.append(os.add_dll_directory(str(native)))
