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
        masterKeyButton = gtk.Button( "Change Master Key" )
        accountKeyButton  = gtk.Button( "Change Account Key" )
        numKeysLabel  = gtk.Label( "Used Key Count" )
        numKeysEntry  = gtk.Entry( )

        numKeysEntry.connect( "insert-text", self.ensure_only_numbers )

        masterKeyBox.pack_start( masterKeyButton )
        masterKeyBox.pack_start( accountKeyButton )
        masterKeyBox.pack_start( numKeysLabel )
        masterKeyBox.pack_start( numKeysEntry )
        masterKeyVBox.pack_start( masterKeyBox, False )
        
        bip32Frame.add( masterKeyVBox )

        self.get_content_area().pack_start( bip32Frame, True, True )
        self.get_content_area().pack_start( proxyFrame, True, True )

        
        masterKeyBox.show()
        masterKeyVBox.show()
        masterKeyButton.show()
        accountKeyButton.show()
        numKeysLabel.show()
        numKeysEntry.show()
        bip32Frame.show()
        proxyFrame.show()


    def ensure_only_numbers( self, widget, new_text, new_text_length, position, data=None ):
        if not re.match( "^\d+$", new_text ):
            widget.emit_stop_by_name( "insert-text" )
