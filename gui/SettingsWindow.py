#!/usr/bin/env python

import pygtk
import gtk
import re

class SettingsWindow(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        self.set_default_size( 500, 400 )
        
        self.add_button( gtk.STOCK_OK, gtk.RESPONSE_OK )
        self.add_button( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL )
        self.add_button( gtk.STOCK_APPLY, gtk.RESPONSE_APPLY )

        bip32Frame = gtk.Frame( "Address Settings" )
        proxyFrame = gtk.Frame( "Connection Settings" )

        masterKeyVBox = gtk.VBox()
        masterKeyBox = gtk.HBox(False, 5 )
        self.masterKeyButton = gtk.Button( "Change Master Key" )
        self.accountKeyButton  = gtk.Button( "Change Account Key" )
        numKeysLabel  = gtk.Label( "Used Key Count" )
        self.numKeysEntry  = gtk.Entry( )

        self.numKeysEntry.connect( "insert-text", self.ensure_only_numbers )

        masterKeyBox.pack_start( self.masterKeyButton )
        masterKeyBox.pack_start( self.accountKeyButton )
        masterKeyBox.pack_start( numKeysLabel )
        masterKeyBox.pack_start( self.numKeysEntry )
        masterKeyVBox.pack_start( masterKeyBox, False )
        
        bip32Frame.add( masterKeyVBox )

        self.get_content_area().pack_start( bip32Frame, True, True )
        self.get_content_area().pack_start( proxyFrame, True, True )

        
        masterKeyBox.show()
        masterKeyVBox.show()
        self.masterKeyButton.show()
        self.accountKeyButton.show()
        numKeysLabel.show()
        self.numKeysEntry.show()
        bip32Frame.show()
        proxyFrame.show()

    def add_controller( self, settingsController ):
        self.masterKeyButton.connect( "clicked", settingsController )

    def ensure_only_numbers( self, widget, new_text, new_text_length, position, data=None ):
        if not re.match( "^\d+$", new_text ):
            widget.emit_stop_by_name( "insert-text" )
