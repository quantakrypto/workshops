import unittest
from crypto_demo import receipt
class Tests(unittest.TestCase):
    def test_signature_and_rejections(self):
        result=receipt({'amount':42})
        self.assertEqual(result['receipt']['amount_msat'],42000)
        for key in ['valid','tamper_rejected','wrong_key_rejected']:
            self.assertTrue(result[key])
if __name__=='__main__': unittest.main()
