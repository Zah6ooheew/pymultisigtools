#!/usr/bin/env python

import pygtk
import gtk

class RedeemScriptWindow(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        self.set_default_size( 700, 400 )
        
        script_frame = self._create_script_frame()
        info_frame = self._create_info_frame()

        self.get_content_area().pack_start( info_frame, False, False )
        self.get_content_area().pack_start( script_frame, True, True )

        info_frame.show()
        script_frame.show()


    #creates the lower half of the frame where the scripts are shown
    def _create_script_frame( self ):
        script_frame = gtk.Frame( "Redeem Scripts" )
        self.script_view = gtk.TreeView()
        self.script_view.set_headers_clickable( False )
        #self.script_view.set_fixed_height_mode( True )

        cell = gtk.CellRendererText()
        address_column = gtk.TreeViewColumn( "Address", cell, text=0 )
        script_column = gtk.TreeViewColumn( "Redeem Script", cell, text=1 )
        notes_column = gtk.TreeViewColumn( "Notes", cell, text=2 )

        self.script_view.append_column( address_column )
        self.script_view.append_column( script_column )
        self.script_view.append_column( notes_column )

        scroll_window = gtk.ScrolledWindow()
        scroll_window.add( self.script_view )
        script_frame.add( scroll_window )

        scroll_window.show()
        self.script_view.show_all()

        return script_frame

    #creates the top area of the frame where we choose the account and filters
    def _create_info_frame( self ):

        info_frame = gtk.Frame( "Redeem Script Info" )
        info_vbox = gtk.VBox()
        address_box = gtk.HBox(False, 5 )
        label_box = gtk.HBox(False, 5 )
        button_box = gtk.HBox(False, 5 )

        self.address_entry = gtk.Entry(max=37)
        self.address_entry.set_width_chars(37)
        self.address_entry.set_sensitive(False)
        script_label = gtk.Label( "Script:" )
        self.script_entry = gtk.Entry()
        self.script_entry.set_width_chars(50)

        notes_label = gtk.Label( "Notes:" )
        self.notes_entry = gtk.Entry()
        self.notes_entry.set_width_chars( 75 )

        self.add_button = gtk.Button( "Add Redeem Script" )

        address_box.pack_start( self.address_entry, False )
        address_box.pack_end( self.script_entry, False )
        address_box.pack_end( script_label, False )
        label_box.pack_start( notes_label, False )
        label_box.pack_start( self.notes_entry, True )
        button_box.pack_end( self.add_button, False )

        info_vbox.pack_start( address_box, False )
        info_vbox.pack_start( label_box, False )
        info_vbox.pack_start( button_box, False )
        
        info_frame.add( info_vbox )
        info_vbox.show_all()

        return info_frame
