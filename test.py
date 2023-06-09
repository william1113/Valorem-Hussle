class User:
    id = None 
    email =None 



def func (**kwargs):
    info = User()

    for key, value in kwargs.items():
        setattr(info,key, value)
   

    print(info.email)
    print(info.id)
    

func(email="test@test.com", id="1")