#!/usr/bin/env python

import pygtk
import gtk

class KeysWindow(gtk.Dialog):
    
    def __init__(self, *args):
        gtk.Dialog.__init__( self, *args )

        self.set_default_size( 700, 400 )
        
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
        #self.key_view.set_fixed_height_mode( True )

        cell = gtk.CellRendererText()
        toggle = gtk.CellRendererToggle()
        count_column = gtk.TreeViewColumn( "", cell, text=0 )
        pubkey_column = gtk.TreeViewColumn( "Public Key", cell, text=1 )
        #address_column = gtk.TreeViewColumn( "Psuedo Address", gtk.CellRendererText(), text=2 )
        used_column = gtk.TreeViewColumn( "Used", toggle, active=2 )

        self.key_view.append_column( count_column )
        self.key_view.append_column( pubkey_column )
        #self.key_view.append_column( address_column )
        self.key_view.append_column( used_column )

        scroll_window = gtk.ScrolledWindow()
        scroll_window.add( self.key_view )
        key_frame.add( scroll_window )

        scroll_window.show()
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
        self.pub_key_button = gtk.Button( "Extended Public Key" )

        info_box.pack_start( self.account_key_button, False )
        info_box.pack_start( label, False )
        info_box.pack_start( self.account_spinner, False )
        info_box.pack_end( self.pub_key_button, False )
        info_vbox.pack_start( info_box, False )
        
        info_frame.add( info_vbox )
        info_vbox.show()
        info_box.show()
        label.show()
        self.account_key_button.show()
        self.pub_key_button.show()
        self.account_spinner.show()
        return info_frame
    
    def _create_popup_menu( self, data_callback ):
        menu = gtk.Menu()
        menu_item = gtk.MenuItem("Show private key")
        menu_item.connect( "activate", self.show_private_key, data_callback )
        menu.append(menu_item)
        return menu

    def create_context_menu( self, event, data_callback ):
        popup_menu = self._create_popup_menu( data_callback )
        popup_menu.popup( None, None, None, event.button, event.time )
        popup_menu.show_all()
        return popup_menu

    def show_private_key( self, event, data=None ):
        private_key = data()
        diag = gtk.MessageDialog( None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK , "Private Key:" )
        diag.format_secondary_markup( private_key )
        diag.run()
        diag.destroy()


