import unittest
from project.customers.models import Customer


class CustomersTestsMethods(unittest.TestCase):
    def test_customer_valid(self):
        customer = Customer("Some Customer", "City", 18)
        self.assertEqual(customer.name, "Some Customer")
        self.assertEqual(customer.city, "City")

    def test_customer_name_invalid(self):
        with self.assertRaises(ValueError):
            Customer("<script>alert('XSS')</script>", "City", 18)

    def test_customer_author_invalid(self):
        with self.assertRaises(ValueError):
            Customer("Some Customer", "<script>alert('XSS')</script>", 18)
