import re

MAX_SUBJECTS = 4

EMAIL_RE = re.compile(r"@university\.com$", re.IGNORECASE)
PASSWORD_RE = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")
