import re
from flask import flash 
def is_valid_email(email):
    pattern = r"[^\s\"']+@[^@]+\.[^@]+"
    if re.match(pattern, email):
        return True
    flash ("Invalid email")
    return False
def is_valid_password(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    if  re.match(pattern, password):
        return True
    flash ("Invalid password")
    return False
def is_valid_name(name):
    pattern = r"^[A-Za-z ]+$"
    
    if re.match(pattern, name):
        return True
    flash ("Invalid name")
    return False
def is_valid_company_name(company_name):
    pattern = r"^[A-Za-z0-9 ]+$"
    if  re.match(pattern, company_name):
        return True
    flash ("Invalid company name")
    return False
    