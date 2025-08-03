def is_valid_email(email):
    """
    Checks if email has no spaces, is under 100 characters, and contains '@'.
    """
    if not email or ' ' in email or len(email) > 100 or '@' not in email:
        return False
    return True

def is_valid_name(name):
    """
    Validates that name is non-empty, under 255 characters, and has no spaces.
    """
    if not name or ' ' in name or len(name) > 255:
        return False
    return True

def is_valid_faculty(faculty):
    """
    Checks if faculty name is non-empty, under 100 chars, and not just spaces.
    """
    if not faculty or len(faculty) > 100:
        return False
    return any(c != ' ' for c in faculty)