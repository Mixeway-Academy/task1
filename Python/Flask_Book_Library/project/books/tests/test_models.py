import pytest
import models


def test_validate_input():
    with pytest.raises(ValueError):
        models.Book._validate_input_value(models.Book, "111")

    with pytest.raises(ValueError):
        models.Book._validate_input_value(models.Book, "x" * 100)
