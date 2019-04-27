#!/usr/bin/env python3.6

import sys
import os.path
import rc4_hash

if __name__== "__main__":
    print ("--- RC4 Password Attacker ---")
    if(len(sys.argv) < 3):
        print("Usage: python rc4_hash_attack.py [FILE] [HASH]")
        sys.exit(1)
    if (os.path.isfile(sys.argv[1]) is False):
        print(sys.argv[1]+" is not a file or does not exist!")
        sys.exit(2)

    #Datei öffnen
    startKnoten = list()
    endKnoten = list()
    with open(sys.argv[1], "r") as file:
        i=0
        for line in file:
            #erstern 2 Zeilen uninteressant
            if (i<2):
                i+=1
                continue
            startKnoten.append(line.split( )[0])
            endKnoten.append(line.split( )[1])
    
    #print(startKnoten)
    #print(endKnoten)
    
    
    findHash = sys.argv[2]
    
    passwordsFound = set()
    
    for i in range(256):     
        try: #Beginnen mit Indexsuche (falls schon als Endknoten bekannt)
            indexFound = endKnoten.index(findHash)
            hashCounter = i
            
            #Wenn gefunden, dann vorne beginnen und bis zur stelle 'hashCounter' hashen
            hash = startKnoten[indexFound]
            for i in range(256-hashCounter):
                password = rc4_hash.strtoarray(hash)
                hash = rc4_hash.paddPass(password)
                hash = rc4_hash.convertPass(hash)
                hash = rc4_hash.prga(rc4_hash.ksa(hash))
                hash = rc4_hash.arraytoHexString(hash)
           
            if (hash == sys.argv[2]): #Nochmals prüfen (iwie notwendig?!)
                passwordsFound.add(rc4_hash.arraytoHexString(password))
                
        except(ValueError):
            pass
        finally: #sonst hashen und erneut suchen
            findHash = rc4_hash.strtoarray(findHash)
            findHash = rc4_hash.paddPass(findHash)
            findHash = rc4_hash.convertPass(findHash)
            findHash = rc4_hash.prga(rc4_hash.ksa(findHash))
            findHash = rc4_hash.arraytoHexString(findHash)
    
    if (len(passwordsFound) > 0):
        for password in passwordsFound:
            print("PASSWORD FOUND: "+password)
    else:
        print("HASH '"+sys.argv[2]+"' NOT FOUND!")
        
    sys.exit(0)