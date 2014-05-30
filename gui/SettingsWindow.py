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

        masterKeyVBox = gtk.VBox(False, 30)
        masterKeyBox = gtk.HBox(False, 5 )
        self.masterKeyButton = gtk.Button( "Change Master Key" )
        accountLabel  = gtk.Label( "Account:" )
        self.accountKeyButton  = gtk.SpinButton( gtk.Adjustment( 1, 0, 256, 1, 5 ) )
        self.accountKeyButton.set_update_policy( gtk.UPDATE_IF_VALID )
        self.accountKeyButton.set_numeric( True )
        self.accountKeyButton.set_snap_to_ticks( True )
        numKeysLabel  = gtk.Label( "Used Key Count" )

        self.numKeysEntry = gtk.SpinButton( gtk.Adjustment( 0, 0, 2**30, 1, 5 ) )
        self.numKeysEntry.set_update_policy( gtk.UPDATE_IF_VALID )
        self.numKeysEntry.set_numeric( True )
        self.numKeysEntry.set_snap_to_ticks( True )

        masterKeyBox.pack_start( self.masterKeyButton )
        masterKeyBox.pack_start( accountLabel )
        masterKeyBox.pack_start( self.accountKeyButton )
        masterKeyBox.pack_end( self.numKeysEntry )
        masterKeyBox.pack_end( numKeysLabel )
        masterKeyVBox.pack_start( masterKeyBox, False )

        backup_box = gtk.HBox(False)
        self.backup_button = gtk.Button( "Show Backup JSON" )
        self.restore_button = gtk.Button( "Restore From JSON" )
        backup_box.pack_start(self.restore_button, False )
        backup_box.pack_end(self.backup_button, False )
        masterKeyVBox.pack_start( backup_box, False )
        
        bip32Frame.add( masterKeyVBox )

        self.get_content_area().pack_start( bip32Frame, True, True )
        self.get_content_area().pack_start( proxyFrame, True, True )

        
        masterKeyBox.show()
        masterKeyVBox.show()
        backup_box.show()
        backup_box.show()
        self.masterKeyButton.show()
        self.backup_button.show()
        self.restore_button.show()
        self.accountKeyButton.show()
        numKeysLabel.show()
        self.numKeysEntry.show()
        bip32Frame.show()
        proxyFrame.show()

    def add_controller( self, settingsController ):
        self.masterKeyButton.connect( "clicked", settingsController )
