from core import crawler, scraper
from html import unescape
import random
import re


NEWEGG_URL = "https://newegg.com"
RTX_30 = "/p/pl?N=100007709%20601357282"
RTX_20 = "/p/pl?N=100007709%20601321572"
RX_6000 = "/p/pl?N=100007709%20601359511"
RX_5000 =  "/p/pl?N=100007709%20601341679"
html = crawler.crawl_html(NEWEGG_URL)

def clean_price(price):
    price_contains_numbers = bool(re.search(r'[\d+,]+(\d+)', price))
    if price_contains_numbers:
        price = unescape(price).split()[0]

    return price

def get_prices(tree):
    price_selector = "//li[contains(@class, 'price-current')]"
    price_text = scraper.get_text(tree, price_selector)

    return list(map(lambda price: clean_price(price), price_text))

def get_names(tree):
    name_selector = "//div[@class='item-info']/a"
    return scraper.get_text(tree, name_selector)

def get_links(tree):
    link_selector = "//div[@class='item-info']/a"
    return scraper.get_attributes(tree, link_selector, "href")

def get_stock_information(tree):
    item_selector = "//div[@class='item-container']"
    child_selector = "div[@class='item-info']/p[contains(., 'OUT OF STOCK')]"
    stock_details = scraper.get_children_text(tree, item_selector, child_selector)

    # set None to in stock, handles case when item has no "out of stock" label
    return list(map(lambda element: element or "IN STOCK", stock_details))

def get_ids(tree):
    item_id_selector = "//ul[@class='item-features']/li[contains(., 'Item #')]/text()"
    return scraper.get_nodes(tree, item_id_selector)

def get_items(tree):
    prices = get_prices(tree)
    names = get_names(tree)
    links = get_links(tree)
    #ids = get_ids(tree)
    stock_details = get_stock_information(tree)
    items = []

    for index, price in enumerate(prices):
        name = names[index]
        link = links[index]
        stock = stock_details[index]
        #gpu_id = ids[index]

        items.append({
            "name": name,
            "link": link,
            "stock": stock,
            'price': price,
            #"gpu_id": gpu_id
        })
    
    return items

which_gpu = input("Which GPU series you want to lookup on NewEgg (RTX 3000, RTX 2000, RX 5000, RX 6000)(If you leave blank or don't input correctly it will randomly select one to show you): ")

if which_gpu.lower() == "rtx 3000" or which_gpu.lower() == "rtx3000":
    gpu_path = RTX_30

elif which_gpu.lower() == "rtx 2000" or which_gpu.lower() == "rtx2000":
    gpu_path = RTX_20

elif which_gpu.lower() == "rx 5000" or which_gpu.lower() == "rx5000":
    gpu_path = RX_5000

elif which_gpu.lower() == "rx 6000" or which_gpu.lower() == "rx6000":
    gpu_path = RX_6000

else:
    rand_select = [RTX_30, RTX_20, RX_5000, RX_6000]
    gpu_path = random.choice(rand_select)

crawl_url = f"{NEWEGG_URL}{gpu_path}"
html = crawler.crawl_html(crawl_url)
tree = scraper.get_tree(html)
items = get_items(tree)

for index in items:
    for key, value in index.items():
        print(key, ":", value)