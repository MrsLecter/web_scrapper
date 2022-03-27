import requests
import re
from bs4 import BeautifulSoup

# constraints
user_agent = 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
accept_language = 'en-US,en;q=0.9'
headers = {"user-agent": user_agent}
product = input('Enter the product name ...')
print('OK!The bot is looking for information. this will take some time')
product = product.replace(' ', '+').lower()


ebay_href = 'https://www.ebay.ca/sch/i.html?_nkw=' + product
page_source = requests.get(ebay_href, headers=headers)

#if you need a original page
f = open('body_file.html', 'w')
for item in page_source:
    f.write(str(item))
f.close()
if page_source.status_code != 200:
    print(f'response failed! Status code {ebay_href.status_code}')
else:
    soup = BeautifulSoup(page_source.text, "lxml")
    name_block = soup.find_all('h3', class_='s-item__title')
    price_block = soup.find_all('span', class_='s-item__price')
    price_delivery = soup.find_all(
        'span', class_='s-item__shipping s-item__logisticsCost')
    link_block = soup.find_all('div', class_='s-item__image')


# parse arr from string
def getPrices(strarr):
    pricearr = []
    for item in strarr:
        item = str(item)
        reg = re.findall('([$\d+.\d{2}])', item)
        reg = ''.join(reg).replace('$', ' $').split(' ')
        for elem in reg:
            if elem:
                pricearr.append(elem)
    pricearr.pop(0)  # advertisment
    return pricearr

# parse delivery price
def getDeliveryPrice(deliverystrarr):
    deliveryarr = []
    for item in deliverystrarr:
        item = str(item)
        reg = re.findall('([$\d+.\d{2}])', item)
        reg = ''.join(reg).replace('$', ' $').split(' ')
        for elem in reg:
            if elem and len(elem) > 4:
                deliveryarr.append(elem)
    deliveryarr.pop(0)  # advertisment
    return deliveryarr


# parse product name
def getProductName(namesarr):
    titlearr = []
    for item in namesarr:
        item = str(item)
        reg = re.findall('(>.*<)', item)
        for elem in reg:
            if elem:
                titlearr.append(elem.replace('>', '').replace('<', ''))
    titlearr.pop(0)  # advertisment
    return titlearr


# parse link from string
def getLink(linkblock):
    linkarr = []
    for item in linkblock:
        item = str(item)
        reg = re.findall('(href=".*?")', item)
        for elem in reg:
            elem = elem.replace('href=\"', '')
            elem = elem.replace('\"', '')
            if elem:
                linkarr.append(elem)
    linkarr.pop(0)  # advertisment link
    return linkarr


names = getProductName(name_block)
prices = getPrices(price_block)
delivery_price = getDeliveryPrice(price_delivery)
links = getLink(link_block)

# write file with founded data
#name | prices | delivery_price | links
filename = "products.csv"
f = open(filename, 'w')
headers = "names, prices, delivery_price,  links\n"
f.write(headers)
iter_notes = 0
for i in range(40):
    f.write(names[iter_notes] + ',' + prices[iter_notes] + ',' +
            delivery_price[iter_notes] + ',' + links[iter_notes]+'\n')
    iter_notes += 1
f.close()
