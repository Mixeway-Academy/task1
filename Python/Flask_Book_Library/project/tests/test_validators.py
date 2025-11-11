import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import pytest
from project.books.models import _clean_text

def test_clean_text_allows_polish_and_alphanumeric():
    """Test: funkcja akceptuje polskie i alfanumeryczne znaki"""
    text = "Zażółć gęślą jaźń 123"
    cleaned = _clean_text(text, "Test field", allow_digits=True)
    assert cleaned == text

def test_rejects_html_tags_and_scripts():
    """Testuje, czy funkcja poprawnie zgłasza błąd dla tekstu zawierającego HTML."""
    field_name = "Opis"
    value = "Wpis z <b>tagiem</b> i <script>alert('x')</script>" 
    
    with pytest.raises(ValueError, match=f"{field_name} cannot contain HTML or script tags"):
        _clean_text(value, field_name)

def test_rejects_invalid_characters_and_checks_allow_digits():
    """Testuje, czy funkcja odrzuca nielegalne znaki i poprawnie stosuje allow_digits=False."""
    field_name = "Imię"
    
    value_with_illegal = "Jan Kowalski!"
    with pytest.raises(ValueError, match=f"{field_name} can only contain letters, digits, spaces, '-', '.', and apostrophes"):
        _clean_text(value_with_illegal, field_name)

    value_with_digit = "Anna-Maria 2"
    with pytest.raises(ValueError, match=f"{field_name} can only contain letters, digits, spaces, '-', '.', and apostrophes"):
        _clean_text(value_with_digit, field_name, allow_digits=False)
