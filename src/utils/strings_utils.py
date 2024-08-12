import re
def format_to_allowed_filename(string: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s]', '_', string).replace(' ', '_')

