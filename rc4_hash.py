#!/usr/bin/env python3.6

import sys
import re

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

#String zu Integerarray, addiert jeweils 2 Hex Ziffern und steckt sie an einen Index
def strtoarray(s):
  o = []
  hexvalue = ''
  for i, char in enumerate(s):
    hexvalue += char
    if(i % 2 is 0): 
      continue
    else:
      o.append(int(hexvalue, 16))
      hexvalue = ''
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

#Erweitert das Array links um Nullen, bis es 3 Byte lang ist
def paddPass(password):
  if(len(password) >= 3): return password
  else:
    while (len(password) is not 3):
      password.insert(0,0)  #an index 0 eine 0 einfügen
    return password

if __name__== "__main__":
  if(len(sys.argv) < 2):
    sys.exit("Usage: python rc4_hash.py password")

  # Prüfen ob gültige Hexwerte
  for v in sys.argv[1]:
    if(not re.search("[0-9a-fA-F]{1,}",v)):
      sys.exit("Value must be a valid Hex-String!")
    
  #Eine Null links anhängen falls Länge ungerade
  if(len(sys.argv[1]) % 2 == 1):
    sys.argv[1] = '0' + sys.argv[1]

  print("Password: 0x"+sys.argv[1][0:6]) #Nur von 0 bis 6 anzeigen da nur das verwendet wird

  #Passwort in Integerarray umwandeln
  password = strtoarray(sys.argv[1])
    
  #Falls array < 3 ist padding hinzufügen
  password = paddPass(password)

  #Passwort in die Form  p1p2p3 -> p1p2p3p1p2p3p1p2 wandeln   
  password = convertPass(password)

  #Hashen
  hash = prga(ksa(password))
  print("Hash: "+arraytoHexString(hash))