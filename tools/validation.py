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

def validator(**kwargs):
    #print(kwargs)
    validation_functions = { "email": (kwargs["email"],is_valid_email),
    "password": (kwargs["password"],is_valid_password),
    "Name": (kwargs["name"], is_valid_name)}
    
    validator: bool = False
    
    for value in validation_functions:
        validator = validation_functions[value][1](validation_functions[value][0])
        print(validator, value)
        if validator:
            continue 
        else:
            validator = False
            break
    
    return validator