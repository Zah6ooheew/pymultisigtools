#!/usr/bin/env python

import pygtk
import gtk

class KeysWindow(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        self.set_default_size( 500, 400 )
        
        key_frame = self._create_key_frame()
        info_frame = self._create_info_frame()

        self.get_content_area().pack_start( info_frame, False, False )
        self.get_content_area().pack_start( key_frame, True, True )

        info_frame.show()
        key_frame.show()


    #creates the lower half of the frame where we can choose the keys to display
    def _create_key_frame( self ):
        key_frame = gtk.Frame( "Account Keys" )
        self.key_view = gtk.TreeView()
        self.key_view.set_headers_clickable( False )
        self.key_view.set_fixed_height_mode( True )

        count_column = gtk.TreeViewColumn( "", gtk.CellRendererText(), text=0 )
        pubkey_column = gtk.TreeViewColumn( "Public Key", gtk.CellRendererText(), text=1 )
        address_column = gtk.TreeViewColumn( "Psuedo Address", gtk.CellRendererText(), text=2 )
        used_column = gtk.TreeViewColumn( "Used", gtk.CellRendererToggle(), active=3 )

        self.key_view.append_column( count_column )
        self.key_view.append_column( pubkey_column )
        self.key_view.append_column( address_column )
        self.key_view.append_column( used_column )

        key_frame.add( self.key_view )
        
        self.key_view.show_all()

        return key_frame


    #creates the top area of the frame where we choose the account and filters
    def _create_info_frame( self ):

        info_frame = gtk.Frame( "Account Info" )
        info_vbox = gtk.VBox()
        info_box = gtk.HBox(False, 5 )
        self.account_key_button = gtk.Button( "Show Account Key" )
        label = gtk.Label( "Account:" )
        self.account_spinner  = gtk.SpinButton( gtk.Adjustment( 1, 0, 256, 1, 5 ) )
        self.account_spinner.set_update_policy( gtk.UPDATE_IF_VALID )
        self.account_spinner.set_numeric( True )
        self.account_spinner.set_snap_to_ticks( True )

        info_box.pack_start( self.account_key_button, False )
        info_box.pack_start( label, False )
        info_box.pack_start( self.account_spinner, False )
        info_vbox.pack_start( info_box, False )
        
        info_frame.add( info_vbox )
        info_vbox.show()
        info_box.show()
        label.show()
        self.account_key_button.show()
        self.account_spinner.show()

        return info_frame

    def add_controller( self, key_window_controller ):
        self.display_button_clicked.connect( "clicked", key_window_controller )
