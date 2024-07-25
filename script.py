from bs4 import BeautifulSoup as bsoup
import requests

my_url = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
response = requests.get(my_url)
html_page = response.text

page_soup = bsoup(html_page, "html.parser")

containers = page_soup.findAll("div", {"class": "_2kHMtA"})

fname = "Laptop.csv"
with open(fname, "w", encoding='utf-8') as f:
    headers = "Prod_Name,Price,Ratings\n"
    f.write(headers)

    for container in containers:
        product_name = container.find("div", {"class": "_4rR01T"})
        if product_name:
            product_name = product_name.text.strip().replace(",", " |")
        else:
            product_name = "N/A"

        price_container = container.find("div", {"class": "_30jeq3"})
        if price_container:
            price = price_container.text.strip()
        else:
            price = "N/A"

        ratings_container = container.find("div", {"class": "_3LWZlK"})
        if ratings_container:
            ratings = ratings_container.text.strip()
        else:
            ratings = "N/A"

        f.write(f"{product_name},{price},{ratings}\n")