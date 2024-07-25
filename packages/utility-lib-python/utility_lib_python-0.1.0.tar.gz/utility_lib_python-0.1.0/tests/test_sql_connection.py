import unittest
from src.sql_connection import DatabaseConnector

class TestSqlFunctions(unittest.TestCase):
    def test_sql_functions(self):
        db_connector = DatabaseConnector()
        db_connector.connect_to_mysql()
        db_connector.close_connection()
        pass

if __name__ == '__main__':
    unittest.main()