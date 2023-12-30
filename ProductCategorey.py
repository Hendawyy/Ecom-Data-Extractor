from bs4 import BeautifulSoup

def get_product_category(soup):

    # Find the first item in the breadcrumb list
    breadcrumb_items = soup.select('#wayfinding-breadcrumbs_container .a-unordered-list.a-horizontal.a-size-small li')

    # Extract the text from the first item
    product_category = breadcrumb_items[0].text.strip() if breadcrumb_items else None

    return product_category

