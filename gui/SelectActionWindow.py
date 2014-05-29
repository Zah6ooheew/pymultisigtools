#!/usr/bin/env python

import pygtk
import gtk
from lib import SelectActionWindowController
from lib import KeyHelper

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
        self.toolbar.append_item( "Create", "Create a new public key", "", gtk.image_new_from_stock( gtk.STOCK_NEW, gtk.ICON_SIZE_LARGE_TOOLBAR) , KeyHelper.show_next_public_key_dialog )
        self.toolbar.append_space()
        self.toolbar.append_item( "Sign", "Sign a partially signed transaction", "", gtk.image_new_from_stock( gtk.STOCK_CONVERT, gtk.ICON_SIZE_LARGE_TOOLBAR ), self.controller.create_sign_window )
        self.toolbar.append_space()
        self.toolbar.append_item( "Keys", "Manage keys", "", gtk.image_new_from_file("gui/encrypted.png") , self.controller.create_key_window )
        self.toolbar.append_space()
        self.toolbar.append_item( "Settings", "Change settings", "", gtk.image_new_from_stock( gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_LARGE_TOOLBAR) , self.controller.create_settings_window )
        self.window.add( self.toolbar )
        self.toolbar.show()
        self.window.show()

    def main( self ):
        gtk.main()
        return 0
