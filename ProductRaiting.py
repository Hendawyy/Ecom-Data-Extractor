from bs4 import BeautifulSoup

def get_product_rating(soup):
    rating_element = soup.find("span", attrs={"class": 'a-icon-alt'})
    if rating_element:
        return rating_element.text
    else:
        return "Rating not available"
