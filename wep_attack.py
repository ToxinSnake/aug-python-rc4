#!/usr/bin/env python3.6

import sys
import re
import os.path
from collections import Counter

if __name__== "__main__":
    print ("--- WEP Attacker ---")
    if(len(sys.argv) < 2):
        print("Usage: python wep_attack.py file")
        sys.exit(1)
    if (os.path.isfile(sys.argv[1]) is False):
        print(sys.argv[1]+" is not a file or does not exist!")
        sys.exit(2)

    #Datei öffnen und mit regex ivs füllen
    ivs = list()
    chitexts = bytearray()
    with open(sys.argv[1], "r") as file:
        file.readline() #erste line skippen
        regex = re.compile('[0-9A-F]{2}')    
        for line in file:
            all = regex.findall(line)
            ivs.append(bytearray.fromhex(all[0]+all[1]+all[2])) #werte 0 bis 2 von all in ivs legen
            chitexts.extend(bytearray.fromhex(all[3]))

    #var initialisierung
    i = 0
    j = 0
    n = 256
    candidatesForK = list()
    
    #ivs sind nun bytearrays in list
    for iv in ivs:

        #s generieren
        s = [i for i in range(256)] 

        #Schritte 0 bis 1
        for t in range(2):
            i = t
            j = (j + s[i] + iv[i % n]) % n
            s[i], s[j] = s[j], s[i]  #swap

        #Schritt 2
        i += 1
        j = (j + s[i] + iv[i % n]) % n

        #wenn S[0] oder S[1] verändert werden: iv verwerfen
        if(j == 0 or j == 1):
            continue
        s[i], s[j] = s[j], s[i]  #swap

        #Schritt 3
        #Annahme: S[0], S[1] & S[3] werden in Schritt 3 bis 256 nicht mehr verändert
        j3 = s[i]
        possibleK = (j3 - j - s[3]) % n
        candidatesForK.append(possibleK)

    #Häufigstes Element in candidatesForK finden
    k = Counter(candidatesForK).most_common(1)[0]
    print("Probable K: "+hex(k[0]))
    print("Found in %d out of %d instances." % (k[1], len(candidatesForK)))
    sys.exit(0)