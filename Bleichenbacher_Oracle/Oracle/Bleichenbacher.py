from TypeChecking.Annotations import typecheck
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class Oracle():
    """
    Bleichebacher's oracle implementing methods available to eve.
    """

    @typecheck
    def __init__(self):
        """
        Setup keys, secret message and encryption/decryption schemes.
        """
        #self._key = RSA.generate(1024)
        n = 127620013709269984265850105693783161236126260522867743149977754589438990838046528207845347412446999189485372849050138923542649968885229674191478016949126898453828655553241416320023751029056807801842722636346936014145779496632203199054885307435781592578204677129277543656632636280481641429969153566525357667293
        e = 65537
        d = 28855049256816189737878860280001813985945632672045626409453749294388009311353486656146182430651992523151719713707141897997390592168413771032688729346051269396689881254390384017476837682959096091564117982045076058124727232948445724627884210664903925925747935922868548526462169054138900851770097825555677441145
        self._key = RSA.construct((n, e, d))
        self._pkcs = PKCS1_v1_5.new(self._key)
        #self._secret = b'This is how Daniel Bleichenbachers adaptive chosen-ciphertext attack works...'
        self._secret = b'Die Definition von Wahnsinn ist, immer wieder das Gleiche zu tun und andere Ergebnisse zu erwarten.'
        self._pkcsmsg = self._pkcs.encrypt(self._secret)

    @typecheck
    def get_n(self) -> int:
        """
        Returns the public RSA modulus.
        """
        return self._key.n

    @typecheck
    def get_e(self) -> int:
        """
        Returns the public RSA exponent.
        """
        return self._key.e

    @typecheck
    def get_k(self) -> int:
        """
        Returns the length of the RSA modulus in bytes.
        """
        return (self._key.size() + 1) // 8

    @typecheck
    def eavesdrop(self) -> bytes:
        return self._pkcsmsg

    @typecheck
    def decrypt(self, ciphertext: bytes) -> bool:
        """
        Modified decrypt method for demonstration purposes.
        See 'Cipher/PKCS1-v1_5.py' for the correct version.

        :param ciphertext: Ciphertext that contains the message to recover.
        :return: True iff the decrypted message is correctly padded according to PKCS#1 v1.5; otherwise False.
        """

        # Step 1
        if len(ciphertext) != self.get_k():
            raise ValueError("Ciphertext with incorrect length.")

        # Step 2a (OS2IP), 2b (RSADP), and part of 2c (I2OSP)
        m = self._key.decrypt(ciphertext)

        # Complete step 2c (I2OSP)
        em = b"\x00" * (self.get_k() - len(m)) + m

        # Step 3 (modified)
        sep = em.find(b"\x00", 2)

        # TODO: Justify oracle strength... --> for testing purposes

        if not em.startswith(b'\x00\x02'):
            return False

        #if not em.startswith(b'\x00\x02') or sep < 10:  # typically sep position will be checked
        #    return False

        # Step 4 (modified)
        return True
