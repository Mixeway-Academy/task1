import unittest
from project.validators import validate_text

class TestBookValidation(unittest.TestCase):
    def test_valid_text(self):
        self.assertEqual(validate_text("Percy Jackson"), "Percy Jackson")

    def test_text_with_spaces(self):
        self.assertEqual(validate_text("  Percy Jackson  "), "Percy Jackson")

    def test_xss_script(self):
        with self.assertRaises(ValueError): 
            validate_text("<script>alert('vulnerability')</script>")

    def test_html_tags(self):
        with self.assertRaises(ValueError): 
            validate_text("<b>Percy Jacksonr</b>")

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            validate_text("")

    def test_whitespace_only(self):
        with self.assertRaises(ValueError):
            validate_text("   ")

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            validate_text(123)
