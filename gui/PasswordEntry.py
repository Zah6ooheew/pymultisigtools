#!/usr/bin/env python

import pygtk
pygtk.require( '2.0' )
import gtk

class PasswordEntry(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        self.entry = gtk.Entry()
        self.entry.set_visibility( False )
        self.entry.set_activates_default( True )
        
        self.add_action_widget( self.entry, gtk.RESPONSE_APPLY )

        self.entry.show()


    def get_text_content( self ): 
        return self.entry.get_text()

