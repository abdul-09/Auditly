from urllib.parse import urlparse
import re

def is_valid_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except:
        return False

def calculate_percentage(value, total):
    """Calculate percentage with proper rounding"""
    try:
        return round((value / total) * 100, 1)
    except ZeroDivisionError:
        return 0

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    # Remove extra whitespace and normalize spaces
    text = re.sub(r'\s+', ' ', text.strip())
    return text
