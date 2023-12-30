from bs4 import BeautifulSoup

def get_product_title(soup):
    title_element = soup.find("span", attrs={"id": 'productTitle'})
    if title_element:
        return title_element.text.strip()
    else:
        return "Product title not found"
