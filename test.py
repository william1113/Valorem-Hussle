import re

def main():
  arg = [{"Apple iPhone 12 Mini, 64GB, Svart (Renoverad)": "5099,00kr"}, 
         {"Apple iPhone XS Max, 128 GB (Renoverad)": "3419,71kr"}, 
         {"Apple iPhone 12 Pro Max, 128GB, Pacific Bl\u00e5 (Renoverad)": "7880,00kr"}, 
         {"Apple iPhone 12 (64GB) - gr\u00f6n": "7990,00kr"}, {"Apple iPhone 12 Pro, 128GB, Pacific Bl\u00e5 (Renoverad)": "8299,00kr"}, 
         {"Google Pixel 6A - Smartphone 128GB, 6GB RAM, Dual Sim, Chalk White": "4490,00kr"}]
  
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
    
        

if __name__ == "__main__":
    print(main())