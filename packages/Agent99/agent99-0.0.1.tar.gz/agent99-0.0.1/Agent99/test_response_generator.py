import unittest
from unittest.mock import patch
from response_generator import ResponseGenerator

class TestResponseGenerator(unittest.TestCase):
    @patch('anthropic.Anthropic.completions.create')
    def test_generate_response_simple(self, mock_create):
        mock_create.return_value.completion = "This is a test response"
        generator = ResponseGenerator(api_key="fake_api_key")
        response = generator.generate_response("Test prompt")
        self.assertEqual(response, "This is a test response")

    @patch('anthropic.Anthropic.completions.create')
    def test_generate_response_api_error(self, mock_create):
        mock_create.side_effect = Exception("APIError")
        generator = ResponseGenerator(api_key="fake_api_key")
        with self.assertRaises(Exception) as context:
            generator.generate_response("Test prompt")
        self.assertTrue("APIError" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
