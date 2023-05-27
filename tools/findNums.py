def findNumsInString(string) -> str:
    string_list = list(string)
    for index_char in range(len(string_list)):
        if 48<=ord(string_list[index_char])<=57:
            string_list.insert(index_char, "+")
            break
    
    return "".join(string_list)


