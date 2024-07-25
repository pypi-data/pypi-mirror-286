import unittest

class Test(unittest.TestCase):
    def test(self):
        from naotw.winman import where 
        import os 
        cmdexe = fr'{os.environ["SystemRoot"]}\System32\cmd.exe'.upper()
        self.assertIn(cmdexe, [exe.upper() for exe in where('cmd')])

if __name__ == '__main__':
    unittest.main()
