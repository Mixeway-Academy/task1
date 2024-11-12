import unittest
from project.common.validators.xss_validator import XSSValidator


class TestXSSValidator(unittest.TestCase):
    def setUp(self):
        self.validator = XSSValidator()

    def test_clean_text(self):
        clean_texts = [
            "Normal text",
            "Hello World!",
            "Text with numbers 123",
            "Text with special chars !@#$%",
            "Text with <> brackets",
        ]

        for text in clean_texts:
            with self.subTest(text=text):
                try:
                    result = self.validator.validate_xss(text)
                    self.assertEqual(result, text)
                except ValueError:
                    self.fail(f"Validator raised XSSException for clean text: {text}")

    def test_xss_detection(self):
        xss_cases = [
            "<script>alert('xss')</script>",
            "javascript:alert(1)",
            "onclick=alert(1)",
            "<img src=x onerror=alert(1)>",
            "<SCRIPT>alert('XSS')</SCRIPT>",
            "JaVaScRiPt:alert(1)",
        ]

        for text in xss_cases:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    self.validator.validate_xss(text)

    def test_invalid_input_type(self):
        invalid_inputs = [
            None,
            123,
            ["list"],
            {"dict": "value"},
            True
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(ValueError):
                    self.validator.validate_xss(invalid_input)

    def test_mixed_content(self):
        mixed_cases = [
            "Normal text with <script>alert(1)</script> in middle",
            "Start javascript:alert(1) end",
            "Multiple <script>alert(1)</script> and onclick=alert(1) cases"
        ]

        for text in mixed_cases:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    self.validator.validate_xss(text)


if __name__ == '__main__':
    unittest.main()
