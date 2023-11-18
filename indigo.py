import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.indigo.ca/en-ca/books/graphic-novels"
base_url_with_tags = "https://www.indigo.ca/en-ca/books/graphic-novels/?storeID=0287&pmin=0.01&prefn1=Language&prefv1=English" # tags are English, available-in-store

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0"
}

# get number of items
r = requests.get(base_url_with_tags, headers=headers, verify=False)
soup = BeautifulSoup(r.content, 'lxml')
target = soup.find("p", class_="m-0 pb-2 pb-lg-0 results-count-border label-4 resultCount").text.split()[0].replace(",", "")

book_list = []

for x in range(0, int(target) // 24 + 1):
    r = requests.get(base_url_with_tags + f'&start={24*x}&sz={24*(x+1)}', headers=headers, verify=False)
    soup = BeautifulSoup(r.content, 'lxml')

    product_list = soup.find_all("div", class_="product-tile")

    for item in product_list:
        title = item.find("img", class_="tile-image").get("title")
        if ("vol" and "1" in title.lower()) or ("vol" not in title.lower()):
            price = item.find("span", class_="value").get("content")
            link = item.find("a", href=True, class_="").get("href")

            book = {
                "title": title,
                "price": price,
                "link": base_url + link
            }

            book_list.append(book)
            print("Saving: " + book["title"])

df = pd.DataFrame(book_list)
df.to_excel("Filtered-Indigo-Books.xlsx")