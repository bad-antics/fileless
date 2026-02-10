import unittest,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from fileless.core import LOLBinExecutor,FilelessDetector

class TestLOLBin(unittest.TestCase):
    def test_techniques(self):
        l=LOLBinExecutor()
        t=l.list_techniques()
        self.assertGreater(len(t),3)

class TestDetector(unittest.TestCase):
    def test_indicators(self):
        d=FilelessDetector()
        self.assertIn("suspicious_cmdlines",d.INDICATORS)
    def test_env(self):
        d=FilelessDetector()
        r=d.check_environment()
        self.assertIsInstance(r,list)

if __name__=="__main__": unittest.main()
