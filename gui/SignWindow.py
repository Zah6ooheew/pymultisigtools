#!/usr/bin/env python

import pygtk
pygtk.require( '2.0' )
import gtk

class SignWindow(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        self.set_default_size( 500, 400 )
        
        self.add_button( gtk.STOCK_OK, gtk.RESPONSE_OK )
        self.add_button( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL )

        self.textView = gtk.TextView()
        self.textView.set_editable( True )
        
        scrollWindow = gtk.ScrolledWindow()
        scrollWindow.add( self.textView )

        self.get_content_area().pack_start( scrollWindow, True, True )

        self.textView.show()
        scrollWindow.show()


    def get_text_content( self ): 
        textBuffer = self.textView.get_buffer()
        start, end = textBuffer.get_bounds()
        return textBuffer.get_text( start, end, False )

