import sys, os, sys, platform
from os import environ
import importlib, importlib.machinery, importlib.util
from delphivcl import moduledefs

def findmodule():
  ossys = platform.system()
  platmac = platform.machine()
  libdir = None
  if ossys == "Windows":
    if (sys.maxsize > 2**32):
      #Win x64
      libdir = "Win64"
    else:
      #Win x86
      libdir = "Win32"

  if libdir:
    sdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), libdir)
    if not os.path.exists(sdir):
      raise ValueError("DelphiVCL module not found. Try to reinstall the delphivcl package or check for support compatibility.")
    for fname in os.listdir(sdir):
      if 'DelphiVCL' in fname:
        return os.path.join(sdir, os.path.basename(fname))
    raise ValueError("DelphiVCL module not found. Try to reinstall the delphivcl package.")
  else:
    raise ValueError("Unsupported platform.")

def new_import():
    modulefullpath = findmodule()
    loader = importlib.machinery.ExtensionFileLoader("DelphiVCL", modulefullpath)
    spec = importlib.util.spec_from_file_location("DelphiVCL", modulefullpath,
        loader=loader, submodule_search_locations=None)
    ld = loader.create_module(spec)
    package = importlib.util.module_from_spec(spec)
    sys.modules["delphivcl"] = package
    spec.loader.exec_module(package)
    return package

#Setup moduledefs.json
if moduledefs.get_auto_load_defs():
  moduledefs.try_load_defs(False)
#Import the shared lib
package = new_import()