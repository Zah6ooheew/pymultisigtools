#!/usr/bin/env python
import gui
import gtk
from Settings import Settings
import exceptions
import bitcoin

class KeyHelper:

    #displays a dialog to display to the user
    #about the next public key
    @staticmethod
    def show_next_public_key_dialog(*args):
        try:
            next_key = KeyHelper.get_next_public_key( )
            diag = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK , "Your new key:" )
            diag.format_secondary_markup( next_key )
            diag.run()
            diag.destroy()
        except Exception as e:
            diag = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK , "Cannot get new key" )
            diag.format_secondary_markup( str( e ) )
            diag.run()
            diag.destroy()
            return False

        return True

        

    @staticmethod
    def get_bip32_key( public_keys ):
        settings = Settings.Instance().get_settings_json()

        if( settings['bip32master'] is None ):
            return None

        account_number, account_key, key_number = KeyHelper.get_account_number_and_chain( settings )

        for i in range( key_number ):
            priv = bitcoin.bip32_ckd( account_key, i )
            priv = bitcoin.bip32_extract_key( priv )
            canidate = bitcoin.privtopub( priv )
            if( canidate in public_keys ):
                return priv

        return None

    @staticmethod 
    def get_accounts():
        settings = Settings.Instance().get_settings_json()
        if( settings['bip32master'] is None ):
            return None

        account_number = settings['accountNumber']

        account_info = {}
        for account in settings['accounts'].keys():
            account_key = settings['accounts'][account]['accountKey']
            chain_length = settings['accounts'][account]['numKeys']

            #make sure we have all our keys
            possible_keys = set(range( chain_length ) )
            actual_keys = set([key[0] for key in settings['accounts'][account].get('keys', [])])
            needed_keys = possible_keys - actual_keys
            if len(needed_keys) > 0:
                if 'keys' not in settings['accounts'][account]:
                    settings['accounts'][account]['keys'] = [] 
                KeyHelper.regenerate_keys( account_key, needed_keys, settings['accounts'][account]['keys'] )
                #save these if we had to regenerate them
                Settings.Instance().save_config_file(settings)
            account_info[account] = settings['accounts'][account].get( 'keys', [] )

        return account_info, account_number

    @staticmethod
    def regenerate_keys( account_key, needed_keys, key_list ):
        for key in needed_keys:
            return_key = bitcoin.bip32_ckd(account_key, key)
            return_key = bitcoin.bip32_extract_key(return_key)
            return_key = bitcoin.privtopub(return_key)
            print return_key
            key_list.append( ( key, return_key, False ) )
        return 
        


    @staticmethod
    def get_account_number_and_chain( settings=None, account_number=None):
        if settings is None:
            settings = Settings.Instance().get_settings_json()
        if account_number is None:
            account_number = settings['accountNumber']
        account_info = settings['accounts'][account_number]
        account_key = account_info['accountKey']
        key_number = account_info['numKeys']

        return account_number, account_key, key_number

    @staticmethod
    def get_private_for_chain( account, key_number ):
        settings = Settings.Instance().get_settings_json()
        account_key = settings['accounts'][account]['accountKey']
        return_key = bitcoin.bip32_ckd( account_key, key_number )
        return_key = bitcoin.bip32_extract_key( return_key )
        return return_key

    @staticmethod
    def get_next_public_key(  ):
        settings = Settings.Instance().get_settings_json()

        if( settings['bip32master'] is None ):
            raise RuntimeError( "Master key has not been set up yet" )

        account_number, account_key, key_number = KeyHelper.get_account_number_and_chain( settings )

        return_key = bitcoin.bip32_ckd( account_key, key_number )
        return_key = bitcoin.bip32_extract_key( return_key )
        return_key = bitcoin.privtopub( return_key )

        #save key for later
        if 'keys' not in settings['accounts'][account_number]:
            settings['accounts'][account_number]['keys'] = []
        settings['accounts'][account_number]['keys'].append( (key_number, return_key, False ) )
        
        #we increment the key counter after making the key
        #because the chain code is 0 indexed, making the 0th key 
        #the first one we use
        key_number += 1

        #remember to save our new key
        settings['accounts'][account_number]['numKeys'] = key_number
        Settings.Instance().save_config_file( settings )

        return return_key

