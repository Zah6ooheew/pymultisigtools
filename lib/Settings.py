#!/usr/bin/env python

import sys
import thread
import time
import io
import os
import nacl.secret
import nacl.utils
import gui
import gtk
import json
import errno
from pbkdf2 import PBKDF2 
from Singleton import Singleton 

@Singleton
class Settings:


    def __init__( self, settingsFile = "settings.json.nacl" ):
        #might as well define this as a constant
        #otherwise we end up with magic numbers elsewhere
        self.PASSWORD_SALT_SIZE = 8
        self.passwordLock = thread.allocate_lock()
        self.key = None
        self.deleteCallbackThread = None
        self.salt = None
        self.cypherText = None
        self.settingsHash = None
        self.settingsFilePath = os.path.join( sys.path[0], settingsFile )
    

    def load_config_file( self ):
        settingsFile = None
        try:
            settingsFile = io.FileIO( self.settingsFilePath, 'r' )
            self.salt = settingsFile.read( self.PASSWORD_SALT_SIZE )
            self.cypherText = settingsFile.readall()
        except IOError as e:
            if( e.errno == errno.ENOENT ):
                return
            alarmDiag = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Cannot open configuration file" )
            alarmDiag.format_secondary_text( os.strerror( e.errno ) )
            alarmDiag.run()
            alarmDiag.destroy()
        finally:
            if settingsFile is not None:
                settingsFile.close() 

    def save_config_file( self, newSettings ):
        self.settingsHash = newSettings
        try:
            if( self.settingsHash is None ):
                raise RuntimeError( "Invalid State", "Tried to save settings that were never set" )

            settingsString = json.dumps( self.settingsHash )

            mykey = self.get_key()
            secretBox = nacl.secret.SecretBox( mykey )
            nonce = nacl.utils.random( nacl.secret.SecretBox.NONCE_SIZE )
            self.cypherText = secretBox.encrypt( settingsString, nonce )
            settingsFile = io.FileIO( self.settingsFilePath, 'w' )
            settingsFile.write( self.salt )
            settingsFile.write( self.cypherText )
            settingsFile.close()
        finally:
            if self.passwordLock.locked():
                self.passwordLock.release()

    def get_settings_json( self ):
        if( self.cypherText is None ):
            self.load_config_file()
        if( self.cypherText is None ):
            return self.get_default_settings()
        try:
            mykey = self.get_key()
            secretBox = nacl.secret.SecretBox( mykey )
            jsonbytes = secretBox.decrypt( self.cypherText )
            configJson = jsonbytes.encode( "utf-8" )
            return json.loads( configJson )
        finally:
            if self.passwordLock.locked():
                self.passwordLock.release()

    #delete the key after it's time'd out 
    def delete_key( self ):
        self.passwordLock.aquire()
        self.key = None
        self.passwordLock.release()

    def get_default_settings( self ):
        defaults = { "bip32master": None, "accountMaster": None, "numKeys": 0 }
        return defaults

    #we may get interrupted forcefully if they key is
    #reaquired before the timeout
    def delete_key_callback( self ):
        try:
            time.sleep( 60 )
            delete_key()
        except SystemExit:
            return

    #everything should use this function if they need the key
    #to ensure that it gets timed out correctly
    #everybody that calls this function is expected to release 
    #the password lock after it's done using the key
    def get_key( self ):
        self.passwordLock.acquire()
        if( self.deleteCallbackThread is not None ):
            self.deleteCallbackThread.exit()

        if( self.key is not None ):
            self.deleteCallbackThread = thread.start_new_thread( self.delete_key_callback, ( ))
            return self.key

        password = gui.PasswordEntry.get_password_from_user( "Configuration Password" )
        if ( self.salt is None ):
            self.salt = nacl.utils.random( self.PASSWORD_SALT_SIZE )
        
        self.key = PBKDF2( password, self.salt ).read( nacl.secret.SecretBox.KEY_SIZE )
        self.deleteCallbackThread = thread.start_new_thread( self.delete_key_callback, () )
        return self.key


    def get_master_bip32_key( self ):
        if( self.cyperText is None ):
            return None

