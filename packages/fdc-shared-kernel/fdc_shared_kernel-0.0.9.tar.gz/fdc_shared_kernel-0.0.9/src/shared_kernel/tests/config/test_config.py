import unittest
import os
from unittest.mock import patch, mock_open
from shared_kernel.config import Config
from shared_kernel.exceptions import InvalidConfiguration, MissingConfiguration


class TestConfig(unittest.TestCase):

    @patch('shared_kernel.config.find_dotenv', return_value='.env')
    def test_init_with_env_file_found(self, mock_find_dotenv):
        with patch('builtins.open', mock_open(read_data='KEY=value')):
            config=Config()
            self.assertEqual(config.get('KEY'), 'value')

    @patch('shared_kernel.config.find_dotenv', return_value='')
    def test_init_with_env_file_not_found(self, mock_find_dotenv):
        with self.assertRaises(InvalidConfiguration):
            Config()

    @patch('shared_kernel.config.find_dotenv', return_value='.env')
    def test_get_existing_variable(self, mock_find_dotenv):
        with patch.dict(os.environ, {'EXISTING_KEY': 'existing_value'}):
            config=Config()
            self.assertEqual(config.get('EXISTING_KEY'), 'existing_value')

    @patch('shared_kernel.config.find_dotenv', return_value='/mocked/path/to/.env')
    def test_get_non_existing_variable(self, mock_find_dotenv):
        with self.assertRaises(MissingConfiguration):
            config=Config()
            config.get('NON_EXISTING_KEY')


if __name__ == '__main__':
    unittest.main()
