import requests
from bs4 import BeautifulSoup
url = "https://www.dailynayadiganta.com/law-and-justice/859367/%E0%A6%9C%E0%A6%BF%E0%A7%9F%E0%A6%BE%E0%A6%89%E0%A6%B2-%E0%A6%B8%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%95-%E0%A6%96%E0%A6%BE%E0%A6%A8%E0%A7%87%E0%A6%B0-%E0%A7%AB-%E0%A6%A6%E0%A6%BF%E0%A6%A8%E0%A7%87%E0%A6%B0-%E0%A6%B0%E0%A6%BF%E0%A6%AE%E0%A6%BE%E0%A6%A8%E0%A7%8D%E0%A6%A1-%E0%A6%AE%E0%A6%9E%E0%A7%8D%E0%A6%9C%E0%A7%81%E0%A6%B0"

response = requests.get(url)
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())

print(soup.find('h1').text)
all_paragraphs = soup.find_all('p')

for paragraph in all_paragraphs:
    print(paragraph.text)


