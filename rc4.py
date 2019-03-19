#!/usr/bin/env python3.6

import sys

def generateSbox(keystream):
    k = list(keystream)  #keystream als list, ein zeichen pro index
    L = len(k)
    s = [i for i in range(256)]

    j = 0
    for i in range(256):
        j = (j + s[i] + ord(k[i%L])) % 256 #ord() konvertiert ascii symbol in integer
        s[i], s[j] = s[j], s[i] #vertausche s[i] mit s[j]
    return s

def encrypt(keystream, plaintext):
    print("Keystream: "+keystream+"\nPlaintext: "+plaintext)
    s = generateSbox(keystream)
    klar = bytearray()
    klar.extend(map(ord, plaintext))
    schl = list()
    i = 0
    j = 0

    for n in range(0, len(klar)):
        i = i + 1 % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        zufallszahl = s[(s[i] + s[j]) % 256]
        schl.append(zufallszahl ^ klar[n]) # ^ = XOR
    return schl

def decrypt(keystream, ciphertext):
    print("Keystream: "+keystream+"\nCiphertext: "+ciphertext)
    s = generateSbox(keystream)
    chi = bytearray.fromhex(ciphertext)
    schl = list()
    i = 0
    j = 0

    for n in range(0, len(chi)):
        i = i + 1 % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        zufallszahl = s[(s[i] + s[j]) % 256]
        schl.append(zufallszahl ^ chi[n]) # ^ = XOR
    return schl


if __name__== "__main__":
    print ("--- RC4 Encryptor ---")
    if(len(sys.argv) < 2):
        print("Usage: python rc4.py [enc|dec] keystream [plaintext|ciphertext]")
        sys.exit(1)

    if(sys.argv[1] == "enc"):
        encrypted = encrypt(sys.argv[2], sys.argv[3])
        encryptedStr = ''
        for i in range(0, len(encrypted)):
            encryptedStr += chr(encrypted[i])
        print("Encrypted Bytesequence:")
        print(''.join(format(x,'02x') for x in encrypted))

    elif(sys.argv[1] == "dec"):
        decrypted = decrypt(sys.argv[2], sys.argv[3])
        decryptedStr = ''
        for i in range(0, len(decrypted)):
            decryptedStr += chr(decrypted[i])
        print("Decrypted Bytesequence:")
        print(''.join(format(x,'02x') for x in decrypted))

    else:
        print("Usage: python rc4.py [enc|dec] keystream [plaintext|ciphertext]") 
        sys.exit(2)
