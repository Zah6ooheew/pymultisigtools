#!/usr/bin/env python
import bitcoin
import json
import KeyHelper

class TxSigner:

    def __init__(self):
        self.tx = None
        self.redeemScript = None
        self.pubs = []
        self.neededSigs = 0
    
    def import_json( self, json_text ):
        try:
            importTxInfo = json.loads( json_text )
        except:
            raise RuntimeError( "Invalid Input", "The input doesn't parse to valid json." )

        try: 
            if 'tx' not in importTxInfo:
                raise ValueError( "No transaction found in json" )

            redeemScriptCanidate = None
    
            try: 
		self.tx = bitcoin.deserialize( importTxInfo['tx'] )
                sigScript = self.tx['ins'][0]['script']
                if sigScript != "":
                    sigScript = bitcoin.deserialize_script( sigScript )
                    redeemScriptCanidate = sigScript[-1]
            except Exception as e:
                raise ValueError( "tx could not be deserialized:" + str( e ) )

            if 'input' in importTxInfo and 'redeemScript' in importTxInfo['input']:
                if redeemScriptCanidate is not None and redeemScriptCanidate.lower() != importTxInfo['input']['redeemScript'].lower():
                    raise ValueError( "redeemScript given in info doesn't match redeemScript from partial signature" )
                redeemScriptCanidate = importTxInfo['input']['redeemScript']

            if redeemScriptCanidate is not None:
                self.pubs, self.neededSigs = KeyHelper.parse_redeem_script( redeemScriptCanidate )
                self.redeemScript = redeemScriptCanidate
            else:
                raise ValueError( "No redeemScript can be located." )

        except ValueError as e:
            raise RuntimeError( "Invalid Input", str( e ) )

    def sign( self, privkey ):
	if( self.tx is None or self.redeemScript is None ):
            raise RuntimeError( "You have not entered in a tx to sign" )

        try:
            pub = bitcoin.privtopub( privkey )
            if pub not in self.pubs:
                pub = bitcoin.encode_pubkey( pub, 'hex_compressed' )
                if pub not in self.pubs: 
                    raise ValueError( "Key doesn't match any public keys in redeemscript" )
            
            stx = bitcoin.serialize( self.tx )
            sigs = self.extract_sigs( self.tx ) 
            sigs.append( bitcoin.multisign( stx, 0, self.redeemScript, privkey ) )
            sigs = self.reorder_sigs( sigs )
            stx = bitcoin.apply_multisignatures( stx, 0, self.redeemScript, sigs )
            return stx, ( len(sigs) >= self.neededSigs )
        except ValueError as e:
            raise RuntimeError( "Key Error", str( e ) )
        except Exception as e: 
            raise RuntimeError( "Unexpected Error", "Unexpected error formating key: " + str( e ) )


    def extract_sigs( self, tx ):
        sigScript = tx['ins'][0]['script']
        if sigScript == "":
            return []

        sigScript = bitcoin.deserialize_script( sigScript )
        return sigScript[1:-1]

    def reorder_sigs( self, sigs ):
        reorderedSigs = []
        stx = bitcoin.serialize( self.tx )
        for pub in self.pubs:
            for sig in sigs:
                if bitcoin.verify_tx_input( stx, 0, self.redeemScript, sig, pub ):
                    reorderedSigs.append( sig )
                    break

        return reorderedSigs
