def addUserToDB(model, **kwargs) -> bool:
    print(kwargs)
    company_required_fields = ["email", "password", "company_name", "owner"]
    user_required_fields = ["email", "password", "firstName", "lastName"]
    password = "hej"
    info = **{field: kwargs.get(field) for field in company_required_fields}
    info["password"] = password
    print(info)
    return True 

addUserToDB("user", email="hej", company_name="tja", owner="okej" )