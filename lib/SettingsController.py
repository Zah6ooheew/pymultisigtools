#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gui
import gtk
import exceptions
import os
import bitcoin
from Settings import Settings

class SettingsController:
    
    def __init__( self, settingsWindow ):
        self.settingsWindow = settingsWindow
        self.settingsWindow.connect_after( "response", self.window_response )
        self.settingsWindow.connect( "delete_event", self.window_delete )
        self.settingsWindow.masterKeyButton.connect( "clicked", self.on_master_key_button_clicked )
        self.changed = False

        self.settingsStore = Settings.Instance().get_settings_json()
        if 'numKeys' in self.settingsStore:
            self.settingsWindow.numKeysEntry.set_text( str( self.settingsStore['numKeys'] ))
        

    def window_delete( self, dialog, data = None ):
        return self.changed

    def window_response( self, dialog, response_id , data = None ):
        #fake it for now
        if response_id == gtk.RESPONSE_CANCEL or response_id == gtk.RESPONSE_DELETE_EVENT:
            if( self.changed ):
                checkIfSure = gtk.MessageDialog( self.settingsWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, "You have unsaved changes, are you sure you want to close?" )
                #checkIfSure.set_image( gtk.image_new_from_stock( gtk.DIALOG_WARNING ) )
                if( checkIfSure.run() == gtk.RESPONSE_NO ):
                    checkIfSure.destroy()
                    return True
                else:
                    self.changed = False

            self.settingsWindow.destroy()
            self.settingsWindow = None
            return


        Settings.Instance().save_config_file( self.settingsStore )

        self.settingsWindow.destroy()
        self.settingsWindow = None
        return

    def on_master_key_button_clicked( self, widget, data=None ):
        if self.settingsStore is not None:
            checkIfSure = gtk.MessageDialog( self.settingsWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, "Choosing a new masterkey will result in complete loss of any keys associated with your old key. Are you sure you wish to do this?" )
            if( checkIfSure.run() == gtk.RESPONSE_NO ):
                checkIfSure.destroy()
                return True
            else:
                checkIfSure.destroy()

        seed = os.urandom( 32 ) 
        masterKey = bitcoin.bip32_master_key( seed )
            
        confirm = gtk.MessageDialog( self.settingsWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Your new key is: " + masterKey )
        confirm.run()
        confirm.destroy()
        self.settingsStore['bip32master'] = masterKey
        self.changed = True
        

    def on_account_key_button_clicked( self, widget, data=None ):
        pass

    

    def generate_key_alert( self ):
        alert = gui.PasswordEntry( "Private Key for Signing", self.signWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT ) 
        alert.run()
        password = alert.get_text_content()
        alert.destroy()
        return password
