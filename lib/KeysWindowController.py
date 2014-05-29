#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gui
import gtk
import exceptions
import os
import bitcoin
import nacl
from KeyHelper import KeyHelper

class KeysWindowController:
    
    def __init__( self, keys_window ):
        self.keys_window = keys_window
        #self.keys_window.connect_after( "response", self.window_response )
        self.keys_window.connect( "delete_event", self.window_delete )
        self.keys_window.account_key_button.connect( "clicked", self.on_account_key_button_clicked )
        self.keys_window.account_spinner.connect( "value_changed", self.update_account )

        self.account_info, account_number = KeyHelper.get_accounts()

        if self.account_info is None:
            this.keys_window.account_spinner.set_sensitive(False)
            display_needs_setup_message()
            return

        self.keys_window.account_spinner.set_value( account_number )



    def display_no_account_message(self):
        pass

    def display_needs_setup_message(self):
        pass

    def window_delete( self, dialog, data = None ):
        return False

    def update_account(self, widget, data=None):
        account = widget.get_value_as_int()
        if account in self.account_info:
            self.keys_window.account_key_button.set_sensitive(True)
        else: 
            self.display_no_account_message()
            self.keys_window.account_key_button.set_sensitive(False)
        return



    def on_account_key_button_clicked( self, widget, data=None ):
        #no account? 
        if self.account_info is None:
            confirm = gtk.MessageDialog( self.keys_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "Setup is not yet complete" )
            confirm.run()
            confirm.destroy()
            return

        try:
            account_number, account_key, key_number = KeyHelper.get_account_number_and_chain( account_number=self.keys_window.account_spinner.get_value_as_int() )
        except nacl.exceptions.CryptoError:
            confirm = gtk.MessageDialog( self.keys_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "Invalid Password" )
            confirm.run()
            confirm.destroy()
            return
            
        confirm = gtk.MessageDialog( self.keys_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Extended Private Account Key:" )
        confirm.format_secondary_markup( account_key )
        confirm.run()
        confirm.destroy()

    def update_widget_values( self ):
        if 'accountNumber' in self.settingsStore:
            account = self.settingsStore['accountNumber']
            self.settingsWindow.accountKeyButton.set_value( account )

        self.changed = True
        return
