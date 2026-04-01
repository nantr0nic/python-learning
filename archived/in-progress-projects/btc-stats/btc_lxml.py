import requests
import lxml.html
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def print_current_price():
    html = requests.get("https://www.google.com/search?q=bitcoin+price", headers=headers)
    doc = lxml.html.fromstring(html.content)
    price_result = doc.xpath('//span[contains(@class, "pclqee")]/text()')
    print(
    f"The price at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} is ${str(price_result[0])}"
    )
    return

def print_past_price():
    html = requests.get("https://www.statmuse.com/money/ask/bitcoin-price-march-9-2015", headers=headers)
    doc = lxml.html.fromstring(html.content)
    search_result = doc.xpath('//tbody[@class="divide-y divide-gray-6 dark:divide-gray-4 leading-[22px]"]')[0]
    temp = search_result.xpath('.//span[contains(@class, "")]/text()')
    for t in temp:
        temp.remove(" ")
    print(temp)

def pick_date():
    month = input("Month >> ").strip().lower()
    day = input("Day >> ").strip()
    year = input("Year >> ").strip()
    site = f"https://www.statmuse.com/money/ask/bitcoin-price-{month}-{day}-{year}"
    html = requests.get(site, headers=headers)
    doc = lxml.html.fromstring(html.content)
    search_result = doc.xpath('//tbody[@class="divide-y divide-gray-6 dark:divide-gray-4 leading-[22px]"]')[0]
    temp = search_result.xpath('.//span[contains(@class, "")]/text()')
    for t in temp:
        temp.remove(" ")
    print(temp)

pick_date()