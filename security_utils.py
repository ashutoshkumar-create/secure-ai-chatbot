import re
import os

# File types we accept
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

# Dangerous code patterns to block
FORBIDDEN_PATTERNS = [
    r'os\.', r'subprocess\.', r'__import__\(', r'exec\(', r'eval\(', 
    r'open\(', r'import\s+sys', r'import\s+shutil', r'import\s+socket'
]

def safe_extension(filename):
    """Check if file has safe extension"""
    ext = filename.split('.')[-1].lower()
    return ext in ALLOWED_EXTENSIONS

def validate_code(code):
    """Scan code for dangerous patterns"""
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, code):
            return False
    return True