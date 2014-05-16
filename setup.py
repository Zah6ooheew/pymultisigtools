from distutils.core import setup
import py2exe
import os
import sys

# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

setup(
    name = 'pymultisigtools',
    description = 'allows a user to sign a tx',
    version = '0.01.01',
    windows = [
                  {
                      'script': 'pymultisigtool.py',
                      'icon_resources': [(0, "pymultisigtool.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes':'cairo, pango, pangocairo, atk, gobject, gio, pycparser, nacl',
		      'skip_archive': True
                  }
              }

)
