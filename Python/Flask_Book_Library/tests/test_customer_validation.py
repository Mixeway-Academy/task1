import unittest
from project.customers.models import Customer

class TestCustomerValidation(unittest.TestCase):
    def test_valid_customer(self):
        customer = Customer("Jan Kowalski", "Warsaw", 23)

        self.assertEqual(customer.name, "Jan Kowalski")
        self.assertEqual(customer.city, "Warsaw")

    def test_text_with_spaces(self):
        customer = Customer("  Jan Kowalski  ", "  Warsaw  ", 23)

        self.assertEqual(customer.name, "Jan Kowalski")
        self.assertEqual(customer.city, "Warsaw")

    def test_xss_in_name(self):
        with self.assertRaises(ValueError):
            Customer("<script>alert('vulnerability')</script>", "Warsaw", 23)

    def test_xss_in_city(self):
        with self.assertRaises(ValueError):
            Customer("Jan Kowalski", "<script>alert('vulnerability')</script>", 23)
