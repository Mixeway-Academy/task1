import pytest
import models


def test_validate_input():
    with pytest.raises(ValueError):
        models.Customer._validate_input_value(models.Customer, "111")

    with pytest.raises(ValueError):
        models.Customer._validate_input_value(models.Customer, "x" * 100)
