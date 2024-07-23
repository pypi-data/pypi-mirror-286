import os
import unittest
import tempfile
from unittest.mock import patch
from website_status_checker import check_website, check_websites


class TestWebsiteStatusChecker(unittest.TestCase):

    @patch("website_status_checker.checker.requests.get")
    def test_check_website_up(self, mock_get):
        mock_get.return_value.status_code = 200
        result = check_website("https://www.example.com")
        self.assertEqual(result, "https://www.example.com is up!")

    @patch("website_status_checker.checker.requests.get")
    def test_check_website_down(self, mock_get):
        mock_get.return_value.status_code = 404
        result = check_website("https://www.nonexistentwebsite.com")
        self.assertEqual(
            result, "https://www.nonexistentwebsite.com is down! Status code: 404"
        )

    @patch("website_status_checker.checker.requests.get")
    def test_check_websites(self, mock_get):
        mock_get.side_effect = [
            type("Response", (object,), {"status_code": 200}),
            type("Response", (object,), {"status_code": 404}),
            Exception("Network error"),
        ]
        urls = [
            "https://www.example.com",
            "https://www.nonexistentwebsite.com",
        ]
        results = check_websites(urls)
        self.assertEqual(results[0], "https://www.example.com is up!")
        self.assertEqual(
            results[1], "https://www.nonexistentwebsite.com is down! Status code: 404"
        )

    @patch("website_status_checker.checker.requests.post")
    def test_check_website_post(self, mock_post):
        mock_post.return_value.status_code = 200
        result = check_website("https://www.example.com", method="POST")
        self.assertEqual(result, "https://www.example.com is up!")

    @patch("website_status_checker.checker.requests.get")
    def test_output_to_file(self, mock_get):
        # Simulate responses for the GET requests
        mock_get.side_effect = [
            type("Response", (object,), {"status_code": 200}),
            type("Response", (object,), {"status_code": 404}),
        ]
        urls = ["https://www.example.com", "https://www.nonexistentwebsite.com"]

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

        # Generate the output to the temporary file
        with open(temp_filename, "w") as f:
            for result in check_websites(urls, method="GET"):
                f.write(result + "\n")

        # Verify that the file contains the expected output
        with open(temp_filename, "r") as f:
            output = f.readlines()

        expected_output = [
            "https://www.example.com is up!\n",
            "https://www.nonexistentwebsite.com is down! Status code: 404\n",
        ]

        self.assertEqual(output, expected_output)

        # Clean up the temporary file
        os.remove(temp_filename)


if __name__ == "__main__":
    unittest.main()
