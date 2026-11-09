import pytest

XSS_PAYLOADS = [
    pytest.param("<script>alert('XSS')</script>", id="script"),
    pytest.param("<ScRiPt>alert(1)</sCrIpT>", id="mixed-case"),
    pytest.param("<img src=x onerror=alert(1)>", id="img-onerror"),
    pytest.param("<svg/onload=alert(1)>", id="svg-onload"),
    pytest.param("<img\nsrc=x\nonerror=alert(1)>", id="newlines"),
    pytest.param("<img src=x onerror=alert(1)//", id="unclosed-img"),
    pytest.param("<svg/onload=alert(1)//", id="unclosed-svg"),
]
