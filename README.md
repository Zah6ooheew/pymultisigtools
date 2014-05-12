pymultisigtools
===============

A new library based on pybitcointools that allows you to easily spend
from P2SH addresses. 

### Planned Features

* Sign partially signed tx
* Create `SIGHASH_NONE` or `SIGHASH_ALL` signatures for new payments from addresses
* Windows-native binary
* Support for a keyring based on BIP0032 HD wallets to automatically sign tx and create keys

###How to use

Right now, only the sign button works. You have to enter in the transaction
using a format similar to the one TMP uses. 

	{
		"tx": "hex of transaction",
		"input": {
			"redeemScript": "hex of redeemscript"
			}
	}

The 'input' securtion is only needed if the redeemScript cannot be 
found in the tx given. For partially signed tx, this info is often optional.

This is also capable of signing the first signature in a tx with no 
signatures on it. redeemScript is mandatory in this case.

The output screen just shows you the raw hex of the transaction. It will 
tell you the transaction isn't complete if it doesn't find the number of 
sigs that the redeemScript mandates. 

It will not push it to the network for you. You will need to use a tool
such as https://blockr.io/tx/push to push it to the network.
