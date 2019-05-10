#!/usr/bin/python3.6

import argparse
import sys

def checkPositive(i):
    if int(i) < 0:
        raise argparse.ArgumentTypeError("{number} is an invalid positive int value".format(number=i))
    return int(i)

def eea(r0, r1):
    
    s = [1, 0]
    t = [0, 1]
    q = [0, 0]
    i = 1
    r = [r0, r1]

    while r[i] != 0:
        i = i + 1
        r.append( r[i-2] % r[i-1] )
        q.append( ((r[i-2] - r[i]) / r[i-1]) % r0 )
        s.append( (s[i-2] - q[i] * s[i-1]) % r0 )
        t.append( (t[i-2] - q[i] * t[i-1]) % r0 )
 
    #gcd, s, t, stepcount
    return (r[i-1], s[i-1], t[i-1], i-1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("r0", help="Any positive integer", type=checkPositive)
    parser.add_argument("r1", help="Any positive integer", type=checkPositive)
    args = parser.parse_args()

    r0 = args.r0
    r1 = args.r1

    if(r0 < r1):
        r0, r1 = r1, r0
    
    eeATuple = eea(r0,r1)     
    if(eeATuple[0] != 1):
        print("gcd: {}, no inverse element exists".format(eeATuple[0]))
        exit(0)

    print("gcd: {gcd}\ns: {s}\nt: {t}\nsteps needed: {steps}".format(gcd=eeATuple[0], s=eeATuple[1], t=eeATuple[2], steps=eeATuple[3]))
    exit(0)