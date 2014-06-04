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

class RedeemScriptWindowController:
    
    def __init__( self, redeem_script_window ):
        self.redeem_script_window = redeem_script_window
        self.redeem_script_window.connect( "delete_event", self.window_delete )

        self.redeem_script_window.add_button.connect( "clicked", self.on_add_button_clicked )
        self.redeem_script_window.script_entry.connect( "changed", self.on_script_changed )

        self.script_info = KeyHelper.get_redeem_scripts()

        if self.script_info is None:
            self.script_info = []
            return

        self.display_redeem_scripts()
        return

    def window_delete(self, dialog, data=None):
        return False

    def display_redeem_scripts(self):
        self.tree_model = gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING )
        for row in self.script_info:
            self.tree_model.append( row )
        self.redeem_script_window.script_view.set_model(self.tree_model)
        self.redeem_script_window.script_view.show_all()

    def on_script_changed( self, widget, data=None ):
        script = widget.get_text()
        address = None
        try: 
            address = bitcoin.scriptaddr( script )
            KeyHelper.parse_redeem_script( script )
        except Exception as e:
            address = "Invalid Script"

        self.redeem_script_window.address_entry.set_text( address )
        return False


    def on_add_button_clicked( self, widget, data=None ):
        redeem_script = None
        address = None

        try: 
             redeem_script = self.redeem_script_window.script_entry.get_text()
             address = bitcoin.scriptaddr( redeem_script )
             KeyHelper.parse_redeem_script( redeem_script )
        except ValueError as e:
            confirm = gtk.MessageDialog( self.keys_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "Invalid redeemScript!" )
            confirm.format_secondary_markup(str(e))
            confirm.run()
            confirm.destroy()
            return

        notes = self.redeem_script_window.notes_entry.get_text()

        try:
            self.script_info = KeyHelper.add_redeem_script( redeem_script, notes )
        except ValueError as e:
            confirm = gtk.MessageDialog( self.redeem_script_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "Duplicate redeemScript!" )
            confirm.format_secondary_markup(str(e))
            confirm.run()
            confirm.destroy()
            return
        except nacl.exceptions.CryptoError:
            confirm = gtk.MessageDialog( self.redeem_script_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "Invalid Password" )
            confirm.run()
            confirm.destroy()
            return

        self.display_redeem_scripts()
        return True
