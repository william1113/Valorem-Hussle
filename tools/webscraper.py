from bs4 import BeautifulSoup
import requests
import pandas as pd
import json 
import codecs

def graber(search):
    search_engine_url = "https://www.amazon.se/s?k="  # Replace with the appropriate search engine URL
    url = search_engine_url + search

    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    product_names = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
    product_prices = soup.find_all('span', class_='a-offscreen')

    products = []
    count = 5
    for name, price in zip(product_names, product_prices):
        if count >=0:
            name = codecs.decode(name.text, 'unicode_escape')
            
            products.append({name.replace("\xa0", "").encode().decode("unicode-escape") : price.text.replace("\xa0", "")})
            count -=1
            continue
        break
        #print(price.text)
        
    return json.dumps(products)
  


print(graber("iphone12"))


