import re

def validate_dni(dni):
    """
    Spanish DNI validation algorithm
    """
    dni_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    if not (isinstance(dni, str) and len(dni) == 9):
        return False
    
    try:
        number = int(dni[:8])
        letter = dni[8].upper()
        calculated_letter = dni_letters[number % 23]
        return letter == calculated_letter
    except ValueError:
        return False

def validate_email(email):
    """
    Email validation using regex
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def calculate_mortgage(principal, apr, term_years):
    """
    Calculate monthly mortgage installment
    """
    monthly_rate = apr / 100 / 12
    months = term_years * 12
    
    installment = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-months))
    
    total_payback = installment * months
    
    return {
        'monthly_installment': round(installment, 2),
        'total_payback_amount': round(total_payback, 2)
    }
