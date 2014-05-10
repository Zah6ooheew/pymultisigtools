#!/usr/bin/env python
import bitcoin
import json

class TxSigner:

    def __init__(self):
        self.tx = None
        self.redeemScript = None
    
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
                pubs = self.parse_redeemScript( redeemScriptCanidate )
                self.redeemScript = redeemScriptCanidate
            else:
                raise ValueError( "No redeemScript can be located." )

        except ValueError as e:
            raise RuntimeError( "Invalid Input", str( e ) )

    def parse_redeemScript( self, script ):
        try:
            elements = bitcoin.deserialize_script( script )
            if elements[-1] != 174:
                raise ValueError( "no OP_CHECKMULTISIG found in redeemScript" )

            if elements[-2] < elements[0]:
                raise ValueError( "redeemscript asks for more sigs than supplies keys" )

            return elements[1:(1+elements[0])]
        except Exception as e:
            raise ValueError( "redeemScript not in valid format: " + str(e) )
