#!/usr/bin/env python
import gui
import gtk
import exceptions

class SettingsController:
    
    def __init__( self, settingsWindow ):
        self.settingsWindow = settingsWindow
        self.settingsWindow.connect_after( "response", self.window_response )
        self.settingsWindow.connect( "delete_event", self.window_delete )
        self.changed = True

    def window_delete( self, dialog, data = None ):
        return self.changed

    def window_response( self, dialog, response_id , data = None ):
        #fake it for now
        if response_id == gtk.RESPONSE_CANCEL or response_id == gtk.RESPONSE_DELETE_EVENT:
            if( self.changed ):
                checkIfSure = gtk.MessageDialog( self.settingsWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, "You have unsaved changes, are you sure you want to close?" )
                #checkIfSure.set_image( gtk.image_new_from_stock( gtk.DIALOG_WARNING ) )
                if( checkIfSure.run() == gtk.RESPONSE_NO ):
                    checkIfSure.destroy()
                    return True
                else:
                    self.changed = False

            self.settingsWindow.destroy()
            self.settingsWindow = None
            return

        self.settingsWindow.destroy()
        self.settingsWindow = None
        return

    def generate_key_alert( self ):
        alert = gui.PasswordEntry( "Private Key for Signing", self.signWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT ) 
        alert.run()
        password = alert.get_text_content()
        alert.destroy()
        return password
