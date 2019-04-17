#!/usr/bin/env python3.6

import sys
import os.path
import rc4_hash

def paddHex(hexstring):
  if(len(hexstring) >= 6): return hexstring
  else:
    while (len(hexstring) is not 6):
      hexstring = '0' + hexstring  #an index 0 eine 0 einfügen
    return hexstring

if __name__== "__main__":
    if(len(sys.argv) < 2):
        sys.exit("Usage: python rc4_bruteforce.py hash")

    N = 2**24 - 1
    compareHash = sys.argv[1]
    print("N: "+str(N)+"\nHash: "+compareHash)

    for i in range(0,N):
        potentialHash = hex(i)[2:]
        potentialHash = paddHex(potentialHash)
        
        findHash = rc4_hash.strtoarray(potentialHash)
        findHash = rc4_hash.paddPass(findHash)
        findHash = rc4_hash.convertPass(findHash)
        findHash = rc4_hash.prga(rc4_hash.ksa(findHash))
        findHash = rc4_hash.arraytoHexString(findHash)

        if(findHash == compareHash):
            print("Passwort found: "+potentialHash)