import re
import requests
from bs4 import BeautifulSoup
base_url = 'https://restapi.amap.com/v3/geocode/regeo?output=xml&location='
fuc_url ='&key=48ee0979f9bcd19ecd349b976a6580bf&radius=1000&extensions=all'
location ='105,25'
url = base_url + location + fuc_url
response = requests.get(url)
soup = BeautifulSoup(response.text,)
address_source = str(soup.find('formatted_address'))
address_make = (re.split('<|>', address_source))
address = address_make[2]
print(address)