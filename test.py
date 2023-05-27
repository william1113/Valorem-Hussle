string = list("iphone12")

for i in range(len(string)):
  if ord(string[i]) >=48 and ord(string[i]) <=57:
    string.insert(i, "+")
    break
string = "".join(string)


print(string)