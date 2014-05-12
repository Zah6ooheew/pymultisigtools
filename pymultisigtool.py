#!/usr/bin/python -W ignore

import gui
import sys
import pygtk
if not sys.platform == 'win32':
    pygtk.require( '2.0' )
import gtk

if __name__ == '__main__':
    mainWindow = gui.SelectActionWindow()
    mainWindow.main()
