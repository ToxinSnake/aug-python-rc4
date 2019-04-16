#!/usr/bin/env python3.6

import sys

def ksa(k):
    s = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + s[i] + k[i % len(k)]) % 256 
        s[i], s[j] = s[j], s[i] #vertausche s[i] mit s[j]
    return s

def prga(s): 
    hash = [0]*3
    i = 0
    j = 0
    for n in range(0, len(hash)):
        i = i + 1 % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        hash[n] = (s[(s[i] + s[j]) % 256])
    return hash

#String zu Integerarray
def strtoarray(s):
  o = []
  for char in s:
    o.append(ord(char))
  return o

#Integerarray zu String
def arraytostr(a):
  s = ''
  for num in a:
    s += chr(num)
  return s

#Integerarray zu Hexstring
def arraytoHexString(a):
    h = '0x'
    for num in a:
        h += "%0.2X" % num
    return h

#Erste drei Bytes vom Passwort nehmen und anhängen, p1p2p3 -> p1p2p3p1p2p3p1p2
def convertPass(password):
    converted = [0]*8
    for i in range(0, len(converted)):
        converted[i] = password[i%3]
    return converted


if __name__== "__main__":
    if(len(sys.argv) < 2):
        print("Usage: python rc4_hash.py password")
        sys.exit(1)

    print("Password: "+sys.argv[1])
    password = strtoarray(sys.argv[1])
    password = convertPass(password)
    hash = prga(ksa(password))
    print("Hash: "+arraytoHexString(hash))