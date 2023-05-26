import requests
from bs4 import BeautifulSoup

def search_ebay(search_string):
    list_of_prices = []

    ebayurl = "https://www.ebay.com/sch/i.html"
    ebaydata =  {"_from":"R40", "_trksid":"m570.l1313", "_nkw":search_string,"_sacat":"0"}
    html = requests.get(ebayurl, params=ebaydata)
    bsObj = BeautifulSoup(html.text, "html.parser")

    item_prices = bsObj.findAll("span", {"class":"s-item__price"})

    for item in item_prices:
        list_of_prices.append(item.getText().split()[0])

    for index, item in enumerate(list_of_prices):
        list_of_prices[index] = list_of_prices[index][1:]

    results = list(map(lambda x: float(x.replace(",", "")), list_of_prices))

    cheapest = '%.2f' % min(results)

    return 'The Cheapest Result for "' + search_string + '" on Ebay: $' + str(cheapest)

if __name__ == '__main__':
    print(search_ebay("baseball bat"))