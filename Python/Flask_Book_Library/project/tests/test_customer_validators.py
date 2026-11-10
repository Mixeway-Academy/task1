import unittest

from loader import load

validators = load('project.customers.validators')
ValidationError = validators.ValidationError


class ValidatorTestCase(unittest.TestCase):
    def assert_valid(self, validator, cases):
        """cases: iterable of (input, expected_output)."""
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(validator(value), expected)

    def assert_invalid(self, validator, values):
        for value in values:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validator(value)


class CustomerNameTests(ValidatorTestCase):
    def test_valid_names_are_accepted(self):
        names = ["Jan Kowalski", "Anna Nowak-Wiśniewska", "O'Brien", "Małgorzata Żółć",
                 "J. R. R. Tolkien", "Smith, John"]
        self.assert_valid(validators.validate_customer_name, [(n, n) for n in names])

    def test_whitespace_is_trimmed_and_collapsed(self):
        self.assert_valid(validators.validate_customer_name, [("  Jan \t Kowalski\n ", "Jan Kowalski")])

    def test_xss_payloads_are_rejected(self):
        self.assert_invalid(validators.validate_customer_name, [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            '" onmouseover="alert(1)',
            "&lt;script&gt;",
            "{{7*7}}",
        ])

    def test_malformed_input_is_rejected(self):
        self.assert_invalid(validators.validate_customer_name, [
            None, "", "   ", 123, ["x"], "Jan123", "...", "A" * 65,
        ])


class CityTests(ValidatorTestCase):
    def test_valid_cities_are_accepted(self):
        cities = ["Warszawa", "Kędzierzyn-Koźle", "Zielona Góra", "St. Louis", "Frankfurt (Oder)"]
        self.assert_valid(validators.validate_city, [(c, c) for c in cities])

    def test_invalid_cities_are_rejected(self):
        self.assert_invalid(validators.validate_city, [
            "<script>alert(1)</script>", "<b>x</b>", "Kraków1", "a=b",
            None, "", "   ", 5, "()", "A" * 65,
        ])


class AgeTests(ValidatorTestCase):
    def test_valid_ages_are_accepted(self):
        self.assert_valid(validators.validate_age, [
            (30, 30), ("30", 30), (" 45 ", 45), (1, 1), (120, 120), ("007", 7),
        ])

    def test_invalid_ages_are_rejected(self):
        self.assert_invalid(validators.validate_age, [
            0, -1, 121, "0", "121", "abc", "<script>alert(1)</script>", "30<b>", "",
            None, True, 30.5, "30.5", "٣٠", [30],
        ])


class ModuleContractTests(unittest.TestCase):
    def test_every_customer_field_has_a_validator(self):
        self.assertEqual(set(validators.CUSTOMER_VALIDATORS), {'name', 'city', 'age'})


if __name__ == '__main__':
    unittest.main()