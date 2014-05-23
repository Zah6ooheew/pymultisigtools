pymultisigtools
===============

A new library based on pybitcointools that allows you to easily spend
from P2SH addresses. 

### Current Features

* Signs tx
* Uses BIP32 compatible structure to generate keys and will automatically use those keys to sign a tx
* Windows Binary (This time full tested!)

### Planned Features

* Create `SIGHASH_NONE` or `SIGHASH_ALL` signatures for new payments from addresses
* Better management of the BIP32 wallet structure.

###How to use

Installation is easy. If you have Tails, or another *nix type system, get
the tarball and run it in place. If you have Windows; use the installer.
I have tested the installer against a fresh Windows 7 installation, so 
It shouldn't cause any problems. If the program doesn't run after installation
on Windows, Let me know. 

On the configuration screen, you can pick a master key for your wallet
and choose which account of that key you plan on using. You can also 
manually adjust where we are in the key chain. You will then work on the 
m/i<sub>h</sub>/0/n key, where n is the number of keys and i is the account
number.

If you want a new key to make an address with, simply hit the create button
after setting up your master key. Everything will automatically be update.d

Your keys are automatically protected by a password that you will be asked to 
enter in when saving for the first time. Right now there is no way to change
this password except to delete your settings file. Choose carefully. Your 
configuration file is stored using the NaCl library. If you forget the password
you aren't getting it back. 

Signing a tx is easy, you just have to git the program json
using a format similar to the one TMP uses. 

	{
		"tx": "hex of transaction",
		"input": {
			"redeemScript": "hex of redeemscript"
			}
	}

The 'input' section is only needed if the redeemScript cannot be 
found in the tx given. For partially signed tx, this info is often optional.

This is also capable of signing the first signature in a tx with no 
signatures on it. redeemScript is mandatory in this case.

The output screen just shows you the raw hex of the transaction. It will 
tell you the transaction isn't complete if it doesn't find the number of 
sigs that the redeemScript mandates. 

It will not push it to the network for you. You will need to use a tool
such as https://blockr.io/tx/push to push it to the network.
