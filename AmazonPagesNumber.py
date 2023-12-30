import requests
from bs4 import BeautifulSoup
import vars as v
import ServiceUnavilableHandler as SUH

def get_last_page_number(URL):
    webpage = SUH.make_request(URL, v.HEADERS)
    if webpage is None:
        return []
    soup = BeautifulSoup(webpage.content, "html.parser")
    pagination_strip = soup.find('span', class_='s-pagination-strip')
    if pagination_strip:
        # Find all elements with the class 's-pagination-item'
        pagination_items = pagination_strip.find_all('a', class_='s-pagination-item')
        # Filter out elements that are not numeric
        numeric_pages = [element.get_text() for element in pagination_items if element.get_text().isdigit()]
        # Return the maximum numeric page
        # print(int(max(numeric_pages)))
        return int(max(numeric_pages, default=1))
    else:
        return 1