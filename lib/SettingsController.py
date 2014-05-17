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
        self.settingsWindow.accountKeyButton.connect( "value_changed", self.update_key_nums )

        self.settingsStore = Settings.Instance().get_settings_json()
        if 'bip32master' in self.settingsStore:
            self.update_widget_values()

        self.changed = False

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

        try:
            self.save_settings()
        except Exception as e:
            alert = gtk.MessageDialog( self.settingsWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Could not save settings: " + str( e ) )
            alert.run()
            alert.destroy()
            Settings.Instance().delete_key()
            return

        if( response_id == gtk.RESPONSE_APPLY ):
            return 

        self.settingsWindow.destroy()
        self.settingsWindow = None
        return

    def save_settings( self ):
        #no settings to save if there is no master key
        if self.settingsStore['bip32master'] is None:
            self.changed= False
            return

        account = self.settingsWindow.accountKeyButton.get_value_as_int()
        self.settingsStore["accountNumber"] = account

        #if there is no info for this account, we have to derive the master key for it
        if( account not in self.settingsStore['accounts'] ):
            self.settingsStore['accounts'][account] = {}
            accountHardenedKey = bitcoin.bip32_ckd( self.settingsStore['bip32master'], ( account + 2**31 ) )
            #we always work with the 'external' chain, since we don't support multiple chains in an account
            accountKey = bitcoin.bip32_ckd( accountHardenedKey, 0 )
            self.settingsStore['accounts'][account]['accountKey'] = accountKey
        
        #update the number of keys
        numKeys = self.settingsWindow.numKeysEntry.get_value_as_int()
        self.settingsStore['accounts'][account]['numKeys'] = numKeys
        Settings.Instance().save_config_file( self.settingsStore )

        self.changed = False
        return

    def update_key_nums( self, widget, data=None ):
        account = widget.get_value_as_int()
        if account in self.settingsStore['accounts']:
            accountValues = self.settingsStore['accounts'][account]
            if 'numKeys' in accountValues:
                numKeys = accountValues['numKeys']
                self.settingsWindow.numKeysEntry.set_value( numKeys )
            else: 
                self.settingsWindow.numKeysEntry.set_value( 0 )
        else: 
            self.settingsWindow.numKeysEntry.set_value( 0 )
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
        self.settingsStore['accountNumber'] = 1
        self.settingsStore['accounts'] = dict()
        self.update_widget_values()

    def update_widget_values( self ):
        if 'accountNumber' in self.settingsStore:
            account = self.settingsStore['accountNumber']
            self.settingsWindow.accountKeyButton.set_value( account )

        self.changed = True
        return
