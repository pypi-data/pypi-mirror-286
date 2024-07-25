import unittest
from src.log_message import Logger

# Constants for log levels
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

class TestLogFunctions(unittest.TestCase):
    def test_log_message(self):
        logger = Logger()
        logger.log("This is an info message.", INFO)
        logger.log("This is a warning message.", WARNING)
        logger.log("This is an error message.", ERROR)
        
        # Add a new log level and log a message with it
        logger.add_log_level("DEBUG")
        logger.log("This is a debug message.", "DEBUG")

        # Remove an existing log level
        logger.remove_log_level("DEBUG")
        pass

if __name__ == '__main__':
    unittest.main()