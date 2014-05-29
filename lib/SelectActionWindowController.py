#!/usr/bin/env python
import gui
import gtk
from TxSigner import *
from Settings import Settings
from KeyHelper import KeyHelper
from SettingsController import SettingsController
from KeysWindowController import KeysWindowController
import nacl.exceptions
import exceptions

class SelectActionWindowController:
    
    def __init__( self, main_window ):
        self.window = main_window
        self.signWindow = None
        self.settingsController = None
        self.settingsWindow = None
        self.key_window = None
        self.key_window_controller = None

    def create_sign_window( self, widget, callback_data = None ):
        if( self.signWindow is not None ):
            self.signWindow.present()
            return

        self.signWindow = gui.SignWindow( "Sign Transaction", self.window, gtk.DIALOG_DESTROY_WITH_PARENT )
        self.signWindow.connect( "response", self.sign_window_response )
        self.signWindow.show()

    def create_key_window( self, widget, callback_data = None ):
        if( self.key_window is not None ):
            self.key_window.present()
            return

        self.key_window = gui.KeysWindow( "Key Management", self.window, gtk.DIALOG_DESTROY_WITH_PARENT )
        try:
            self.key_window_controller = KeysWindowController( self.key_window )
        except nacl.exceptions.CryptoError as e:
            diag = gtk.MessageDialog( self.signWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK , "Invalid Password" )

            diag.run()
            diag.destroy()
            Settings.Instance().delete_key()
            self.key_window.destroy()
            self.key_window = None
            return

        self.key_window.connect("destroy", self.key_window_destroyed)
        self.key_window.show()

    def create_settings_window( self, widget, callback_data = None ):
        if( self.settingsWindow is not None ):
            self.settingsWindow.present()
            return

        self.settingsWindow = gui.SettingsWindow( "Settings", self.window, gtk.DIALOG_DESTROY_WITH_PARENT )
        try:
            self.settingsController = SettingsController( self.settingsWindow )
        except:
            diag = gtk.MessageDialog( self.signWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK , "Invalid Password" )
            diag.run()
            diag.destroy()
            Settings.Instance().delete_key()
            self.settingsWindow.destroy()
            self.settingsWindow = None
            return
        self.settingsWindow.connect( "destroy", self.settings_window_destroyed )
        self.settingsWindow.show()

    #we have to delete our references if this is destroyed
    def settings_window_destroyed( self, dialog, data = None ):
        self.settingsWindow = None
        self.settingsController = None
        return False

    #we have to delete our references if this is destroyed
    def key_window_destroyed( self, dialog, data = None ):
        self.key_window = None
        #self.key_window_controller = None
        return False

    def sign_window_response( self, dialog, response_id , data = None ):
        #fake it for now
        if response_id == gtk.RESPONSE_CANCEL or response_id == gtk.RESPONSE_DELETE_EVENT:
            self.signWindow.destroy()
            self.signWindow = None
            return

        bufferText = dialog.get_text_content()
        signer = TxSigner()
        try:
            signer.import_json( bufferText )
            key = KeyHelper.get_bip32_key( signer.pubs )
            if( key is None ):
                key = gui.PasswordEntry.get_password_from_user( "Private Key" )
            signedtx, complete = signer.sign( key )
            self.show_signed_tx( signedtx, complete )
            
        except RuntimeError as e:
            primaryError = e.args[0]
            secondaryError = e.args[1]
            diag = gtk.MessageDialog( self.signWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK , primaryError )
            diag.format_secondary_markup( secondaryError )
            diag.run()
            diag.destroy()
            self.signWindow.present()
            return

        self.signWindow.destroy()
        self.signWindow = None
        return

    def show_signed_tx( self, tx, complete ):
	if( complete ):
	    windowTitle = "Signed Transaction"
	else:
	    windowTitle = "Incompletely Signed Transaction"
        results = gui.ResultsWindow( windowTitle, self.signWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT )
        results.set_text_content( tx )
        results.run()
        results.destroy()

