import unittest
from src.excel_functions import ExcelReader, WriteToExcel

class TestExcelFunctions(unittest.TestCase):
    def test_excel_reader(self):
        excel_reader_6_columns = ExcelReader('./assets/sample-debt-upload-data.xlsx', selected_columns=['city', 'state'])
        excel_reader_6_columns.read_excel()
        values = excel_reader_6_columns.iterate_rows()

        for row_data in values:
            print(row_data)
        pass

    def test_write_to_excel(self):
        excel = WriteToExcel("example.xlsx")
        file = excel.createWorkbook()
        sheet = excel.createWorksheet(file, "my_sheet")
        row, col = excel.defineRowColumn(0, 0)

        scores = [
            ['ankit', 1000],
            ['rahul', 100],
            ['priya', 300],
            ['harshita', 50],
        ]

        for name, score in scores:
            sheet.write(row, col, name)
            sheet.write(row, col + 1, score)
            row += 1

        excel.closeWorkbook(file)
        pass

if __name__ == '__main__':
    unittest.main()