#!/usr/bin/env python

import pygtk
import gtk

class ResultsWindow(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        self.set_default_size( 500, 400 )
        
        self.add_button( gtk.STOCK_OK, gtk.RESPONSE_OK )

        self.textView = gtk.TextView()
        self.textView.set_wrap_mode( gtk.WRAP_CHAR )
        self.textView.set_editable( False )
        self.get_content_area().pack_start( self.textView, True, True )
        self.textView.show()


    def set_text_content( self, text ): 
        textBuffer = self.textView.get_buffer()
        return textBuffer.set_text( text )

