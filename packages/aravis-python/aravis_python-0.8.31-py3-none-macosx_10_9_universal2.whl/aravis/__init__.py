import os
import ctypes
import platform
pre_built_path = os.path.dirname(__file__)
if platform.system() == 'Windows':
    os.add_dll_directory(os.path.join(pre_built_path, "bin"))
    aravis_module = os.path.join(pre_built_path, "bin/aravis-0.8-0.dll")
elif platform.system() == 'Darwin':
    aravis_module = os.path.join(pre_built_path, 'lib/libaravis-0.8.dylib')
elif platform.system() == 'Linux':
    aravis_module = os.path.join(pre_built_path, "lib/libaravis-0.8.so")

ctypes.cdll.LoadLibrary(aravis_module)

gi_typelib = os.path.join(os.path.dirname(__file__), 'lib')
os.environ['GI_TYPELIB_PATH'] = gi_typelib
import gi
gi.require_version("Aravis", "0.8")
from gi.repository import Aravis
