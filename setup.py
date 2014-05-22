from distutils.core import setup
import py2exe
import os
import sys
from glob import glob

# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]
__import__('nacl._lib')
m = sys.modules['nacl._lib']
nacl_path = m.__path__[0]
data_files = [( "nacl\\_lib\\", glob( os.path.join( nacl_path, "*.h" ) ) )]
data_files += [( "nacl\\_lib\\", glob( os.path.join( nacl_path, "*.pyd" ) ) )]
data_files += [ os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll') ]


origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    if os.path.basename(pathname).lower() in ("libsodium.dll"):
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL


setup(
    name = 'pymultisigtools',
    description = 'allows a user to sign a tx',
    version = '0.02.01',
    windows = [
                  {
                      'script': 'pymultisigtool.py',
                      'icon_resources': [(0, "pymultisigtool.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings, nacl._lib, pycparser',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
		      'includes': 'cairo, pango, pangocairo, atk, gtk, gobject, gio, gtk.keysyms',
		      'skip_archive': True,
                  }
              },
    data_files = data_files
)

