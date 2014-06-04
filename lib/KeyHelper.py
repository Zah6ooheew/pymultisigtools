#!/usr/bin/env python
import gui
import gtk
import exceptions
import bitcoin
import json
from Settings import Settings

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

        #see if we already have this cached, and I can just get the key fast
        cached = set( settings['accounts'][account_number].get(keys,[]) )
        pub_set = set( public_keys )
        hits = cached & pub_set 

        if len(hits) > 0:
            return KeyHelper.get_private_for_chain( account_number, hits[0][0], settings )

        #drat, didn't find it! at least we can only need to test the ones that 
        #we didn't already check
        missed = set(range(key_number)) - set([cache[0] for cache in cached])
            
        for i in missed:
            priv = bitcoin.bip32_ckd( account_key, i )
            priv = bitcoin.bip32_extract_key( priv )
            canidate = bitcoin.privtopub( priv )
            if( canidate in public_keys ):
                return priv

        return None

    @staticmethod
    def get_extended_public_key( account_key ):
        return bitcoin.bip32_privtopub( account_key )

    @staticmethod
    def get_redeem_scripts():
        settings = Settings.Instance().get_settings_json()
        if 'redeemScripts' not in settings:
            return None

        return settings["redeemScripts"]

    @staticmethod
    def add_redeem_script( script, notes ):
        settings = Settings.Instance().get_settings_json()

        if 'redeemScripts' not in settings:
            settings['redeemScripts'] = []

        #check for correctness of redeem_script
        #this will raise an exception if there is a bad script
        KeyHelper.parse_redeem_script( script )

        p2shaddr = bitcoin.scriptaddr( script )

        #see if this is a duplicate
        duplicates = [ dup for dup in settings['redeemScripts'] if dup[0] == p2shaddr ]
        if len( duplicates ) > 0:
            raise ValueError( "%s already in redeem script list!" % p2shaddr )

        settings['redeemScripts'].append( [ p2shaddr, script, notes ] )
        Settings.Instance().save_config_file( settings )

        return settings['redeemScripts']

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
            key_list.append( ( key, return_key, False ) )
        return 
        

    @staticmethod
    def parse_redeem_script( script ):
        try:
            elements = bitcoin.deserialize_script( script )
            if elements[-1] != 174:
                raise ValueError( "no OP_CHECKMULTISIG found in redeemScript" )

            if elements[-2] < elements[0]:
                raise ValueError( "redeemscript asks for more sigs than supplies keys" )

            return elements[1:(1+elements[-2])], elements[0]
        except Exception as e:
            raise ValueError( "redeemScript not in valid format: " + str(e) )

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
    def get_private_for_chain(account, key_number, settings=None):
        if settings is None:
            settings = Settings.Instance().get_settings_json()
        account_key = settings['accounts'][account]['accountKey']
        return_key = bitcoin.bip32_ckd( account_key, key_number )
        return_key = bitcoin.bip32_extract_key( return_key )
        return return_key

    @staticmethod
    def clean_settings( backup_json ):
        clean_settings = {}
        new_settings = json.loads( backup_json, object_hook=lambda x: Settings.Instance().fix_account_keys(x) )
        if 'bip32master' not in new_settings:
            raise ValueError( "Given JSON doesn't have master key" )
        vbytes, depth, fingerprint, i, chaincode, key = bitcoin.bip32_deserialize( new_settings['bip32master'] )
        if vbytes != bitcoin.PRIVATE or depth != 0 or i != 0 or fingerprint != '\x00'*4:
            raise ValueError( "Master key is not at top of tree and private" )

        clean_settings['bip32master'] = new_settings['bip32master']
        clean_settings['accountNumber'] = new_settings.get( "accountNumber", 1 )
        clean_settings['accounts'] = { }
        
        for account, account_info in new_settings.get( 'accounts', { } ).items():
            if 'accountKey' not in account_info:
                raise ValueError( "Account %i has no master key" % account )
            vbytes, depth, fingerprint, i, chaincode, key = bitcoin.bip32_deserialize( account_info["accountKey"]  )
            if depth != 2 or vbytes != bitcoin.PRIVATE or i != 0:
                raise ValueError( "Account %i has invalid master key" % account )

            if account_info.get( "numKeys", 0 ) < 0:
                raise ValueError( "Account %i has invalid key count " % account )
            clean_settings['accounts'][account] = { }
            clean_settings['accounts'][account]['accountKey'] = account_info['accountKey']
            clean_settings['accounts'][account]['numKeys'] = account_info.get( "numKeys", 0 )
            clean_settings['accounts'][account]['keys'] = []
            KeyHelper.regenerate_keys( account_info['accountKey'], range( account_info.get("numKeys", 0 )), clean_settings['accounts'][account]['keys'] )

            #FIXME: actually check validity of imported redeemscripts
            clean_settings['redeemScripts'] = new_settings.get( 'redeemScripts', [] )

        return clean_settings

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

