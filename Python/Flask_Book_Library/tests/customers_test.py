"Customers Model Test"

import unittest

from project.customers.models import CustomerChecker, Customer

correct_input = {"name": "Customer Name", "city": "City Name", "age": 21}
xss_input = {
    "name": "CN <script>alert('xss')</script>",
    "city": "CC <script>alert('xss')</script>",
    "age": "12 <script>alert('xss')</script>",
}
invalid_input = {
    "age": "abc",
}


class TestCustomerModel(unittest.TestCase):

    def test_customer_model(self):
        customer = Customer(**correct_input)
        self.assertEqual(customer.name, correct_input["name"])
        self.assertEqual(customer.city, correct_input["city"])
        self.assertEqual(customer.age, correct_input["age"])

    def test_customer_model_xss(self):
        customer = Customer(**correct_input)
        # expect exception
        with self.assertRaises(ValueError):
            customer = Customer(**xss_input)

    def test_name(self):
        input = correct_input.copy()
        input["age"] = invalid_input["age"]
        with self.assertRaises(ValueError):
            customer = Customer(**input)
