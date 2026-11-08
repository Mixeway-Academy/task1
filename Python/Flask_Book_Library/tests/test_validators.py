import importlib.util
from pathlib import Path

import pytest

_path = Path(__file__).resolve().parent.parent / 'project' / 'validators.py'
_spec = importlib.util.spec_from_file_location('validators', _path)
validators = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validators)


def test_xss_payload_is_rejected():
    with pytest.raises(ValueError):
        validators.validate_text('<script>alert(1);</script>', 'name')
