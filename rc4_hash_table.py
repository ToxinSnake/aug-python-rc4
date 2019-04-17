#!/usr/bin/env python3.6

import sys
from random import randint
import rc4_hash

def rand_password():
    h = ""
    for i in range(3):               
        h += "%0.2X" % randint(0,255)
    return h


def generate_start_values(quantity):
    values = set()
    while(len(values)<quantity):
        values.add(rand_password())
    return values


def generate_hashes(valueList, quantity):
    hashes = list()
    for value in valueList:
        hash = value
        for i in range(quantity):
            hash = rc4_hash.strtoarray(hash)
            hash = rc4_hash.paddPass(hash)
            hash = rc4_hash.convertPass(hash)
            hash = rc4_hash.prga(rc4_hash.ksa(hash))
            hash = rc4_hash.arraytoHexString(hash)
        hashes.append(hash)
        #zwischendurch Status drucken 
        if (len(hashes) % int(len(valueList)/20) == 0):
            print(str(int(len(hashes)/len(valueList)*100))+"% ("+str(len(hashes))+" values)")
    return hashes


def writeFile(filename, list1, list2):
    file = open(filename, "w")
    file.write("PASSWD  HASH  ("+str(len(list1))+" entries)\n---------------------------------\n")
    i=0
    for value in list1:
       file.write(value+" "+list2[i]+"\n")
       i += 1
    file.close()


if __name__== "__main__":    
    print("--- RC4 hashtable generator ---\n")
    
    #Passwortraum
    N = 2**24 
    
    #Zeilen n
    n = round(N**(2/3))
    
    #Spalten m
    m = round(N**(1/3))
    
    print("N =",N,"\nn =",n,"\nm =",m)    
    
    print("\n(1/3) generating start values ...")
    startValues = generate_start_values(n)
    print("- done")
    #print(startValues)
    
    print("\n(2/3) create hash chains ...")
    hashList = generate_hashes(startValues, m)
    print("- done")
    #print(hashList)
    
    print("\n(3/3) write data to file ...")
    writeFile("table1.txt",startValues,hashList)
    print("- done")
    
