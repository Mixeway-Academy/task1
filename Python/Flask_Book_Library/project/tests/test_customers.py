import unittest

from project.customers.models import Customer


class TestCustomer(unittest.TestCase):
    
    class TestName:

        def test_validate_name_normal(self):
            name = 'First Something Last IV'

            self.assertEqual(Customer._validate_name(name), None)

        def test_validate_name_0_characters(self):
            name = ''

            with self.assertRaises(ValueError):
                Customer._validate_name(name)

        def test_validate_name_more_than_64_characters(self):
            name = 'x'*65

            with self.assertRaises(ValueError):
                Customer._validate_name(name)

        def test_validate_name_script_injection(self):
            name = '<script>alert()</script>'

            with self.assertRaises(ValueError):
                Customer._validate_name(name)

    class TestCity:

        def test_validate_city_normal(self):
            name = 'Old Town with Big River'

            self.assertEqual(Customer._validate_city(name), None)

        def test_validate_city_0_characters(self):
            name = ''

            with self.assertRaises(ValueError):
                Customer._validate_city(name)

        def test_validate_city_more_than_64_characters(self):
            name = 'x'*65

            with self.assertRaises(ValueError):
                Customer._validate_city(name)

        def test_validate_city_script_injection(self):
            name = '<script>alert()</script>'

            with self.assertRaises(ValueError):
                Customer._validate_city(name)
