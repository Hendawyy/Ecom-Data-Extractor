from bs4 import BeautifulSoup

def get_product_sold_count(soup):
    # Find the span with the number of products bought
    sold_count_span = soup.select_one('#social-proofing-faceout-title-tk_bought span')

    # Extract the text from the span
    sold_count = sold_count_span.text.strip() if sold_count_span else None

    return sold_count