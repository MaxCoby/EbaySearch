import requests
from bs4 import BeautifulSoup
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

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

    return min(results)

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))  # beep\n

def notify_no_parameters():
    search_string = "pencil"
    threshold = 10.00
    cheapest = search_ebay(search_string)
    if cheapest < threshold:
        cheapest = '%.2f' % cheapest
        return notify('Item Found', 'The Cheapest Result for ' + search_string + ' on Ebay: $' + str(cheapest))
    else:
        threshold = '%.2f' % threshold
        return notify('No Item Found', 'No Result Found Under $' + str(threshold))

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(notify_no_parameters, 'cron', day_of_week='mon-fri', hour=14, minute=9, second=25)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()