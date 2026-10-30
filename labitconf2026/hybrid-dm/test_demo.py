import unittest
from crypto_demo import dm_keys, dm, dm_open
class Tests(unittest.TestCase):
    def test_roundtrip_and_tamper(self):
        keys=dm_keys()
        result=dm({'keys':keys,'message':'Hola 🌎'})
        options={'keys':keys,'envelope':result,'ciphertext':result['ciphertext_hex']}
        self.assertEqual(dm_open(options),{'valid':True,'recovered':'Hola 🌎'})
        changed=('1' if options['ciphertext'][0]=='0' else '0')+options['ciphertext'][1:]
        self.assertFalse(dm_open({**options,'ciphertext':changed})['valid'])
        self.assertFalse(dm_open({**options,'keys':dm_keys()})['valid'])
    def test_same_keys_new_nonce(self):
        keys=dm_keys()
        a=dm({'keys':keys,'message':'Uno'})
        b=dm({'keys':keys,'message':'Dos'})
        self.assertEqual(a['x25519_public_hex'],b['x25519_public_hex'])
        self.assertNotEqual(a['nonce_hex'],b['nonce_hex'])
if __name__=='__main__': unittest.main()
