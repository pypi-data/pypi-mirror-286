import unittest

import emonk.crypto


class TestCrypto(unittest.TestCase):
    def test_encrypt(self):
        s = "When in the course of human events"
        pw = "my terrible password"
        emonk.crypto.genkey(pw)
        enc = emonk.crypto.encrypt(s)
        dec = emonk.crypto.decrypt(enc, pw)
        self.assertEqual(dec, s)


if __name__ == "__main__":
    unittest.main()
