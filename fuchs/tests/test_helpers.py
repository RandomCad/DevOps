import requests
import unittest
from unittest.mock import patch, MagicMock
from fuchs.helpers import (
    put_file_on_hamster,
    delete_file_on_hamster,
    convert_md_to_html,
)


class TestHelpers(unittest.TestCase):
    @patch("fuchs.helpers.requests.put")
    def test_put_file_on_hamster_success(self, mock_put):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = ""
        mock_put.return_value = mock_response

        result = put_file_on_hamster("test_path", b"test_file")
        self.assertEqual(result, {"status": "success", "html": ""})

    @patch("fuchs.helpers.requests.put")
    def test_put_file_on_hamster_http_error(self, mock_put):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("HTTP Error")
        )
        mock_put.return_value = mock_response

        result = put_file_on_hamster("test_path", b"test_file")
        self.assertEqual(result["status"], "error")
        self.assertIn("HTTP error occurred", result["message"])

    @patch("fuchs.helpers.requests.put")
    def test_put_file_on_hamster_request_error(self, mock_put):
        mock_put.side_effect = requests.exceptions.RequestException(
            "Request Error"
        )

        result = put_file_on_hamster("test_path", b"test_file")
        self.assertEqual(result["status"], "error")
        self.assertIn("Request error occurred", result["message"])

    @patch("fuchs.helpers.requests.put")
    def test_put_file_on_hamster_invalid_input(self, mock_put):
        mock_put.side_effect = Exception("Invalid input")
        result = put_file_on_hamster("test_path", b"test_file")
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid input: Invalid input", result["message"])

    @patch("fuchs.helpers.requests.delete")
    def test_delete_file_on_hamster_success(self, mock_delete):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = ""
        mock_delete.return_value = mock_response

        result = delete_file_on_hamster("test_path")
        self.assertEqual(result, {"status": "success", "html": ""})

    @patch("fuchs.helpers.requests.delete")
    def test_delete_file_on_hamster_http_error(self, mock_delete):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("HTTP Error")
        )
        mock_delete.return_value = mock_response

        result = delete_file_on_hamster("test_path")
        self.assertEqual(result["status"], "error")
        self.assertIn("HTTP error occurred", result["message"])

    @patch("fuchs.helpers.requests.delete")
    def test_delete_file_on_hamster_request_error(self, mock_delete):
        mock_delete.side_effect = requests.exceptions.RequestException(
            "Request Error"
        )

        result = delete_file_on_hamster("test_path")
        self.assertEqual(result["status"], "error")
        self.assertIn("Request error occurred", result["message"])

    @patch("fuchs.helpers.requests.delete")
    def test_delete_file_on_hamster_invalid_input(self, mock_delete):
        mock_delete.side_effect = Exception("Invalid input")
        result = delete_file_on_hamster("test_path")
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid input: Invalid input", result["message"])

    @patch("fuchs.helpers.requests.post")
    def test_convert_md_to_html_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<p>HTML Content</p>"
        mock_post.return_value = mock_response

        result = convert_md_to_html("**Markdown**")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["html"], "<p>HTML Content</p>")

    @patch("fuchs.helpers.requests.post")
    def test_convert_md_to_html_http_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("HTTP Error")
        )
        mock_post.return_value = mock_response

        result = convert_md_to_html("**Markdown**")
        self.assertEqual(result["status"], "error")
        self.assertIn("HTTP error occurred", result["message"])

    @patch("fuchs.helpers.requests.post")
    def test_convert_md_to_html_request_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException(
            "Request Error"
        )

        result = convert_md_to_html("**Markdown**")
        self.assertEqual(result["status"], "error")
        self.assertIn("Request error occurred", result["message"])

    @patch("fuchs.helpers.requests.post")
    def test_convert_md_to_html_invalid_input(self, mock_post):
        mock_post.side_effect = Exception("Invalid input")
        result = convert_md_to_html("**Markdown**")
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid input: Invalid input", result["message"])


if __name__ == "__main__":
    unittest.main()
