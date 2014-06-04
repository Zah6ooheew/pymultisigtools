#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gui
import gtk
import gobject
import exceptions
import os
import bitcoin
import nacl
from KeyHelper import KeyHelper
from operator import itemgetter

class KeysWindowController:
    
    def __init__( self, keys_window ):
        self.keys_window = keys_window
        #self.keys_window.connect_after( "response", self.window_response )
        self.keys_window.connect( "delete_event", self.window_delete )
        self.keys_window.account_key_button.connect( "clicked", self.on_account_key_button_clicked )
        self.keys_window.pub_key_button.connect( "clicked", self.on_account_key_button_clicked, True )
        self.keys_window.key_view.connect( "button_press_event", self.display_context_menu )
        self.keys_window.account_spinner.connect( "value_changed", self.update_account )

        self.account_info, account_number = KeyHelper.get_accounts()

        if self.account_info is None:
            self.keys_window.account_spinner.set_sensitive(False)
            display_needs_setup_message()
            return

        self.keys_window.account_spinner.set_value( account_number )


    def display_account_keys(self, account_number):
        self.tree_model = gtk.ListStore( gobject.TYPE_INT, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN )
        for key in sorted(self.account_info[account_number]):
            self.tree_model.append( key )

        self.keys_window.key_view.set_model(self.tree_model)
        self.keys_window.key_view.show_all()

    #this pops up a context menu
    def display_context_menu(self, widget, event, data=None):
        if event.window != self.keys_window.key_view.get_bin_window():
            return False

        if event.button != 3: 
            return False

        context_path_tuple = widget.get_path_at_pos( event.x, event.y )
        if context_path_tuple is not None:
            self.keys_window.create_context_menu( event, lambda: self.get_private_key( context_path_tuple ) ) 

    def get_private_key( self, context_path ):
        itr = self.keys_window.key_view.get_model().get_iter(context_path[0])
        chain_code = self.keys_window.key_view.get_model().get_value(itr, 0)
        account = self.keys_window.account_spinner.get_value_as_int()
        private_key = KeyHelper.get_private_for_chain( account, chain_code )
        return private_key
        

    def display_no_account_message(self):
        
        pass

    def display_needs_setup_message(self):
        pass

    def window_delete(self, dialog, data=None):
        return False

    def update_account(self, widget, data=None):
        account = widget.get_value_as_int()
        if account in self.account_info:
            self.keys_window.account_key_button.set_sensitive(True)
            self.display_account_keys( account )
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

        label_string = "Extended Private Account Key:"
        #This means we are showing a public key
        if data is True: 
            label_string = "Public Extended Account Key:"
            account_key = KeyHelper.get_extended_public_key( account_key )
            
        confirm = gtk.MessageDialog( self.keys_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, label_string )
        confirm.format_secondary_markup( account_key )
        confirm.run()
        confirm.destroy()
