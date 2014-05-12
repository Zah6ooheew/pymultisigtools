#!/usr/bin/env python
import gui
import gtk
from TxSigner import *
import exceptions

class SelectActionWindowController:
    
    def __init__( self, main_window ):
        self.window = main_window
        self.signWindow = None

    def create_sign_window( self, widget, callback_data = None ):
        if( self.signWindow is not None ):
            self.signWindow.present()
            return

        self.signWindow = gui.SignWindow( "Sign Transaction", self.window, gtk.DIALOG_DESTROY_WITH_PARENT )
        self.signWindow.connect( "response", self.sign_window_response )
        self.signWindow.show()

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
            key = self.generate_key_alert( )
            signedtx, complete = signer.sign( key )
            self.show_signed_tx( signedtx, complete )
            
        except RuntimeError as e:
            self.generate_error_alert( e.args )
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

    def generate_error_alert( self, *args ):
        string1, string2 = args[0]
        alert = gtk.Dialog( string1, self.signWindow, gtk.DIALOG_MODAL, ( gtk.STOCK_OK, gtk.RESPONSE_OK ) )
        label = gtk.Label( string2 )
        alert.vbox.pack_start( label )
        label.show()
        alert.run()
        alert.destroy()

    def generate_key_alert( self ):
        alert = gui.PasswordEntry( "Private Key for Signing", self.signWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT ) 
        alert.run()
        password = alert.get_text_content()
        alert.destroy()
        return password
