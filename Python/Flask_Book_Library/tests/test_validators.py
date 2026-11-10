import unittest

from project.validators import (
    MAX_TEXT_LENGTH,
    validate_choice,
    validate_number,
    validate_text,
)

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    '<img src=x onerror=alert(1)>',
    '"><svg onload=alert(1)>',
    '<a href="javascript:alert(1)">click</a>',
    '&lt;script&gt;alert(1)&lt;/script&gt;',
    '`alert(1)`',
]


class ValidateTextTest(unittest.TestCase):

    def test_accepts_valid_text(self):
        for value in [
            'Pan Tadeusz',
            'Adam Mickiewicz',
            "J.R.R. O'Brien-Tolkien",
            'Harry Potter: Part 1 (2nd ed.)',
            'Zażółć gęślą jaźń',
            'a' * MAX_TEXT_LENGTH,
        ]:
            with self.subTest(value=value):
                self.assertEqual(validate_text(value, 'name'), value)

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(validate_text('  Pan Tadeusz \n', 'name'), 'Pan Tadeusz')

    def test_rejects_xss_payloads(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError) as cm:
                    validate_text(payload, 'name')
                # The error message must not reflect the rejected input back.
                self.assertNotIn(payload, str(cm.exception))

    def test_rejects_newline_inside_value(self):
        with self.assertRaises(ValueError):
            validate_text('Pan Tadeusz\n<script>alert(1)</script>', 'name')

    def test_rejects_too_long_text(self):
        with self.assertRaises(ValueError):
            validate_text('a' * (MAX_TEXT_LENGTH + 1), 'name')

    def test_rejects_empty_or_non_text(self):
        for value in ['', '   ', None, 123, ['<script>']]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_text(value, 'name')

    def test_error_message_contains_field_name(self):
        with self.assertRaisesRegex(ValueError, 'author'):
            validate_text('<b>', 'author')


class ValidateNumberTest(unittest.TestCase):

    def test_accepts_int_and_numeric_string(self):
        for value, expected in [(2003, 2003), ('2003', 2003), (' 42 ', 42), (0, 0)]:
            with self.subTest(value=value):
                self.assertEqual(validate_number(value, 'year_published'), expected)

    def test_rejects_non_numbers(self):
        for value in ['<script>alert(1)</script>', 'two thousand', '20.5', '', None, True, 20.5, ['1']]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_number(value, 'year_published')


class ValidateChoiceTest(unittest.TestCase):
    CHOICES = ('2days', '5days', '10days')

    def test_accepts_allowed_values(self):
        for value in self.CHOICES:
            with self.subTest(value=value):
                self.assertEqual(validate_choice(value, 'book_type', self.CHOICES), value)

    def test_rejects_other_values(self):
        for value in ['<script>alert(1)</script>', '2DAYS', '1day', '', None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_choice(value, 'book_type', self.CHOICES)


if __name__ == '__main__':
    unittest.main()
