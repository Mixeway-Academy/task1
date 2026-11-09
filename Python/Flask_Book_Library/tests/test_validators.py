import pytest
from project.validators import validate


def test_text_with_punctuation_and_number_passes():
    assert validate("Dziady, cz. 3") == "Dziady, cz. 3"


def test_none_passes():
    assert validate(None) is None


def test_xss_payload_rejected():
    with pytest.raises(ValueError, match='Forbidden characters'):
        validate("<script>alert('Miłego dzionka i smacznej kawusi!')</script>")
