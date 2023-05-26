from bs4 import BeautifulSoup
import requests
import pandas as pd
import json 
import re


def unicodeChanger(arg):
    for index, indexValue in enumerate(arg):
        for key, value in indexValue.items():        
            unconverted_str = key
        
            converted_str = ""

            reg = re.findall("\\\\[0-9].{2}", unconverted_str)
            char_esc_sqc = [chr(int(elem[2:])) for elem in reg]
            
            for char in char_esc_sqc:
                converted_str = re.sub("\\\\[0-9].{2}", char, unconverted_str, 1)
                arg[index][key] = arg[index][converted_str]
                del arg[index][key] 
            
    return arg 

def graber(search):
    
    search_engine_url = "https://www.amazon.se/s?k="  # Replace with the appropriate search engine URL
    url = search_engine_url + search

    response = requests.get(url)
    html_content = response.content
    
    soup = BeautifulSoup(html_content, 'html.parser')

    product_names = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
    product_prices = soup.find_all('span', class_='a-offscreen')

    with open("./config.json", "r") as config_file:
        count = json.load(config_file)["count"]

    products = []
    for name, price in zip(product_names, product_prices):
        if count >=0:
        
            
            products.append({name.text.replace("\xa0", ""): price.text.replace("\xa0", "")})
            count -=1
            continue
        break
        #print(price.text)
    products = unicodeChanger(products)
    #print(products)
    return unicodeChanger(products)
  