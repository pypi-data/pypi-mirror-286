import unittest

class Test(unittest.TestCase):
    def test(self):
        from naotw.gpt import 檔案內容轉譯議會備詢提問並複製剪貼簿
        from pathlib import Path
        import clipboard
        import os, sys
        f = Path(__file__).parent / '112財稅局重審核定.docx'
        檔案內容轉譯議會備詢提問並複製剪貼簿(f)
        self.assertEqual(len(clipboard.paste()), 4612)
        clipboard.copy("") 
        os.system(f'{sys.executable} -m naotw.gpt --file2inquery "{f}"') 
        self.assertEqual(len(clipboard.paste()), 4612)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
