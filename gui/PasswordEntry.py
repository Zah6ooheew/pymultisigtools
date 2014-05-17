#!/usr/bin/env python

import pygtk
pygtk.require( '2.0' )
import gtk

class PasswordEntry(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        label = gtk.Label( args[0] )
        self.get_content_area().add( label )
        label.show()

        self.entry = gtk.Entry()
        self.entry.set_visibility( False )
        self.entry.set_activates_default( True )
        
        self.add_action_widget( self.entry, gtk.RESPONSE_APPLY )

        self.entry.show()


    def get_text_content( self ): 
        return self.entry.get_text()

    @staticmethod 
    def get_password_from_user( prompt ):
        alert = PasswordEntry( prompt, None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT ) 
        alert.run()
        password = alert.get_text_content()
        alert.destroy()
        return password


