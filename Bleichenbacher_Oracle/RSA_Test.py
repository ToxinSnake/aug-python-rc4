from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

test = RSA.generate(1024)
pkcs = PKCS1_v1_5.new(test)
pkcsmsg = pkcs.encrypt(b'Die Definition von Wahnsinn ist, immer wieder das Gleiche zu tun und andere Ergebnisse zu erwarten.')
n = 127620013709269984265850105693783161236126260522867743149977754589438990838046528207845347412446999189485372849050138923542649968885229674191478016949126898453828655553241416320023751029056807801842722636346936014145779496632203199054885307435781592578204677129277543656632636280481641429969153566525357667293

print (type(n))
print(n)