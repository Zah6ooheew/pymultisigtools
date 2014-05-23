#!/usr/bin/python -W ignore

import gui
import lib
import sys
import pygtk
if not sys.platform == 'win32':
    pygtk.require( '2.0' )
import gtk
import warnings
warnings.simplefilter('ignore')


if __name__ == '__main__':
    gtk.threads_init()
    mainWindow = gui.SelectActionWindow()
    mainWindow.main()
    lib.Settings.Instance().cancel_callback()
    gtk.threads_leave()
