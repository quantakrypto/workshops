import unittest
from crypto_demo import scanner, classify
class Tests(unittest.TestCase):
    def test_exposure_and_history(self):
        result=scanner()
        self.assertEqual([x['exposure'] for x in result['rows']],['exposed','not-observed','exposed','unknown'])
        self.assertEqual(classify(result['rows'][2]['scriptPubKey'],[])['exposure'],'not-observed')
        self.assertEqual(classify('xyz',[])['exposure'],'unknown')
if __name__=='__main__': unittest.main()
