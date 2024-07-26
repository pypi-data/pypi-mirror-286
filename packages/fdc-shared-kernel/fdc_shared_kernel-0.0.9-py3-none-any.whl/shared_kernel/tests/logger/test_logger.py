import unittest
from unittest.mock import patch, MagicMock
import logging
from shared_kernel.logger import Logger


class TestLogger(unittest.TestCase):

    @patch('logging.getLogger')
    def setUp(self, mock_get_logger):
        # Setup runs before each test method
        self.mock_logger = MagicMock(spec=logging.Logger)
        self.mock_logger.handlers = []  # Initialize handlers attribute
        self.mock_logger.level = logging.NOTSET  # Set the level attribute
        mock_get_logger.return_value = self.mock_logger
        self.test_logger = Logger(name='test_logger', log_file='test_log.log')

    def test_init(self):
        # Test initialization parameters
        self.assertEqual(self.test_logger.name, 'test_logger')
        self.assertEqual(self.test_logger.log_file, 'test_log.log')

    def test_configure_logger(self):
        # Test logger configuration
        self.test_logger.configure_logger()
        self.mock_logger.addHandler.assert_called()

    def test_info_logging(self):
        # Test info logging
        message = 'Test info message'
        self.test_logger.info(message)
        self.mock_logger.info.assert_called_with(message)

    def test_error_logging(self):
        # Test error logging
        message = 'Test error message'
        self.test_logger.error(message)
        self.mock_logger.error.assert_called_with(message)

    def test_debug_logging(self):
        # Test debug logging
        message = 'Test debug message'
        self.test_logger.debug(message)
        self.mock_logger.debug.assert_called_with(message)


if __name__ == '__main__':
    unittest.main()
