import unittest
from src.file_functions import FileRenamer

class TestFileFunctions(unittest.TestCase):
    def test_excel_reader(self):
        path = r'D:\images\Walpapers'
        file_renamer = FileRenamer(path, name_format="{prefix}-{count:03d}")
        file_renamer.rename_files()
        pass

if __name__ == '__main__':
    unittest.main()