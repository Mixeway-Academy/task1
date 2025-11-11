import pytest
from project.books.models import strip_html  

#testy jednostkowe dla strip html (walidator)
def test_strip_html_removes_html_tags():
    assert strip_html("<b>Hello</b>") == "Hello"
    assert strip_html("<script>alert(1)</script>") == "alert(1)"
    assert strip_html("<img src=x onerror=alert(1)>") == ""
    assert strip_html("No tags here") == "No tags here"
    assert strip_html("") == ""
    assert strip_html(None) is None
