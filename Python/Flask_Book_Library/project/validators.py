import re

TEXT_RE = re.compile(r"^[\w '.,:;!?()\-]{1,64}$") # letters, digits, spaces and ' . , : ; ! ? ( ) - 


def validate_text(value, field):
    value = str(value or '').strip()
    if not TEXT_RE.match(value):
        raise ValueError(f'{field} is empty, too long or contains invalid characters')
    return value
