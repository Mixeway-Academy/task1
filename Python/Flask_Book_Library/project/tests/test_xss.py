from markupsafe import escape
import pytest


def test_escape_normal_text():
    assert escape("Hello world") == "Hello world"


def test_escape_empty_string():
    assert escape("") == ""


def test_escape_safe_html():
    assert escape("<b>bold</b>") == "&lt;b&gt;bold&lt;/b&gt;"


def test_escape_script_tag():
    assert escape("<script>alert('XSS')</script>") == "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;"
