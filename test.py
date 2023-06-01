def func (**kwargs):
    user = {"email": None, "password": None }
    for key, value in kwargs.items():
            setattr(user,key, value)
    
    print(user)
    
func(email="hej", password = "då")