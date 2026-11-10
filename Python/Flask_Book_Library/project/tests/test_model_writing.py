import ast
import unittest

from loader import PROJECT_DIR, load

MODELS = {
    'books': ('Book', 'project.books.validators', 'BOOK_VALIDATORS'),
    'customers': ('Customer', 'project.customers.validators', 'CUSTOMER_VALIDATORS'),
    'loans': ('Loan', 'project.loans.validators', 'LOAN_VALIDATORS'),
}


def inspect_model(package, class_name):
    source = (PROJECT_DIR / package / 'models.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name)

    columns, validated, init_source = set(), set(), ''
    for node in cls.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and getattr(node.value.func, 'attr', '') == 'Column':
            columns |= {t.id for t in node.targets if isinstance(t, ast.Name)}
        if isinstance(node, ast.FunctionDef):
            if node.name == '__init__':
                init_source = ast.get_source_segment(source, node)
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and getattr(dec.func, 'id', '') == 'validates':
                    validated |= {a.value for a in dec.args if isinstance(a, ast.Constant)}
    return columns - {'id'}, validated, init_source


class ModelWiringTests(unittest.TestCase):
    def test_validates_hook_covers_every_column_and_validator(self):
        for package, (class_name, module, table) in MODELS.items():
            with self.subTest(model=class_name):
                columns, validated, _ = inspect_model(package, class_name)
                validators = set(getattr(load(module), table))
                self.assertEqual(validated, columns, "@validates must list every column")
                self.assertEqual(validators, columns, "validator table must cover every column")

    def test_loan_init_checks_the_loan_period(self):
        _, _, init_source = inspect_model('loans', 'Loan')
        self.assertIn('validate_loan_period(self.loan_date, self.return_date)', init_source)


if __name__ == '__main__':
    unittest.main()