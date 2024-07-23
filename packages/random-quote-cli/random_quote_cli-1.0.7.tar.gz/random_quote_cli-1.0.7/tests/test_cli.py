import unittest
from unittest.mock import patch
from click.testing import CliRunner
from random_quote.cli import main  # Assuming your main function is in cli.py

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @patch('requests.get')
    def test_main_with_author_mock(self, mock_get):
        mock_get.return_value.json.return_value = {
            'content': 'Mocked quote content',
            'author': 'Mocked author'
        }
        result = self.runner.invoke(main, ['--author', 'Albert Einstein'])
        self.assertEqual(result.exit_code, 0)
        assert 'Mocked quote content' in result.output
        assert '- Mocked author' in result.output

    @patch('requests.get')
    def test_main_without_author_mock(self, mock_get):
        mock_get.return_value.json.return_value = {
            'content': 'Mocked quote content',
            'author': 'Mocked author'
        }
        result = self.runner.invoke(main)
        self.assertEqual(result.exit_code, 0)
        assert 'Mocked quote content' in result.output
        assert '- Mocked author' in result.output

    def test_main_with_author(self):
        result = self.runner.invoke(main, ['--author', 'Albert Einstein'])
        self.assertEqual(result.exit_code, 0)

    def test_main_without_author(self):
        result = self.runner.invoke(main)
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()
