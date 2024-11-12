import re


class XSSValidator:
    XSS_PATTERNS = [
        (r'<script[^>]*>.*?</script>', 'Script tag detected'),
        (r'javascript:', 'JavaScript protocol detected'),
        (r'on\w+\s*=', 'Event handler detected'),
        (r'(alert|eval|Function)\s*\(', 'Dangerous function detected'),
        (r'<iframe[^>]*>', 'iFrame detected'),
        (r'<img[^>]*>', 'Image tag detected'),
        (r'expression\s*\(', 'Expression detected'),
        (r'document\.', 'Document object access detected'),
        (r'window\.', 'Window object access detected'),
    ]

    @classmethod
    def validate_xss(cls, text: str) -> str:
        if not isinstance(text, str):
            raise ValueError(f"Input is not valid string")

        for pattern, message in cls.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                raise ValueError(f"XSS detected: {message}")

        return text
