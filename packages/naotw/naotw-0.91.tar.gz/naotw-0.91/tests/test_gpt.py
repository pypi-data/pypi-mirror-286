import unittest

class Test(unittest.TestCase):
    def test(self):
        from naotw.gpt import 檔案內容轉譯議會備詢提問並複製剪貼簿
        from pathlib import Path
        import clipboard
        import os, sys
        f = Path(__file__).parent / '112財稅局重審核定.docx'
        檔案內容轉譯議會備詢提問並複製剪貼簿(f)
        self.assertEqual(len(clipboard.paste()), 3338)
        clipboard.copy("") 
        os.system(f'{sys.executable} -m naotw.gpt --file2inquery "{f}"') 
        self.assertEqual(len(clipboard.paste()), 3338)

    def test_clipboard_trans(self):
        from naotw.gpt import 剪貼簿內容轉譯議會備詢提問
        import clipboard
        import os, sys
        t = clipboard.copy('a aa')
        os.system(f'{sys.executable} -m naotw.gpt --clipboard2inquery') 
        self.assertEqual(len(clipboard.paste()), 2277)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
