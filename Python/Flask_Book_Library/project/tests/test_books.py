import unittest

from project.books.models import Book


class TestBook(unittest.TestCase):
    
    class TestName:

        def test_validate_name_normal(self):
            name = 'Something: Book of 1, 2 and 3'

            self.assertEqual(Book._validate_name(name), None)

        def test_validate_name_0_characters(self):
            name = ''

            with self.assertRaises(ValueError):
                Book._validate_name(name)

        def test_validate_name_more_than_64_characters(self):
            name = 'x'*65

            with self.assertRaises(ValueError):
                Book._validate_name(name)

        def test_validate_name_script_injection(self):
            name = '<script>alert()</script>'

            with self.assertRaises(ValueError):
                Book._validate_name(name)

    class TestAuthor:

        def test_validate_author_normal(self):
            name = 'First Something Last IV'

            self.assertEqual(Book._validate_author(name), None)

        def test_validate_author_0_characters(self):
            name = ''

            with self.assertRaises(ValueError):
                Book._validate_author(name)

        def test_validate_author_more_than_64_characters(self):
            name = 'x'*65

            with self.assertRaises(ValueError):
                Book._validate_author(name)

        def test_validate_author_script_injection(self):
            name = '<script>alert()</script>'

            with self.assertRaises(ValueError):
                Book._validate_author(name)
