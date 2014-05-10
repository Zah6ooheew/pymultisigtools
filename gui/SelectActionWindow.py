#!/usr/bin/env python

import pygtk
pygtk.require( '2.0' )
import gtk
from lib import SelectActionWindowController

class SelectActionWindow:
    
    #deal with being asked to close
    def delete_event( self, widget, event, data=None ):
        return False


    #if I need to be destroyed, I will be
    def destroy( self, widget, data=None ):
        gtk.main_quit()



    def __init__(self):

        self.window= gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.controller = SelectActionWindowController( self.window )

        self.toolbar = gtk.Toolbar()
        self.toolbar.set_orientation( gtk.ORIENTATION_HORIZONTAL )
        self.toolbar.set_style( gtk.TOOLBAR_BOTH )
        self.toolbar.append_item( "Sign", "Sign a partially signed transaction", "", gtk.image_new_from_stock( gtk.STOCK_CONVERT, gtk.ICON_SIZE_LARGE_TOOLBAR ), self.controller.create_sign_window )
        self.toolbar.append_space()
        self.toolbar.append_item( "Create", "Create a new spend tx", "", gtk.image_new_from_stock( gtk.STOCK_NEW, gtk.ICON_SIZE_LARGE_TOOLBAR) , self.newTransactionCallback )
        self.window.add( self.toolbar )
        self.toolbar.show()
        self.window.show()


    def newTransactionCallback( self, widget, callback_data = None ):
        pass

    def main( self ):
        gtk.main()
        return 0
