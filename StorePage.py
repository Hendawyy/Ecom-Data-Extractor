from bs4 import BeautifulSoup
import vars as v
import ServiceUnavilableHandler as SUH

def scrape_page(url):
    webpage = SUH.make_request(url, v.HEADERS)
    if webpage is None:
        return []

    print(webpage)
    # print(webpage.text)
    soup = BeautifulSoup(webpage.content, "html.parser")
    category = None
    product_data = []

    for product in soup.find_all('div', {'data-asin': True}):
        asin = product['data-asin']
        prime_icon = product.find('i', class_='a-icon-prime')
        is_prime = True if prime_icon else False

        # Check if the product is a best seller
        best_seller_label = product.find('span', {'class': 'a-badge-text', 'data-a-badge-color': 'sx-cloud'})
        best_seller_category = product.find('span', {'class': 'a-badge-supplementary-text'})

        if best_seller_label:
            is_best_seller = True
            category = best_seller_category.text.strip() if best_seller_category else None
            best_seller_info = f"Best Seller{' '+ category if category else ''}"
        else:
            is_best_seller = False
            best_seller_info = None

        product_data.append({
            "data-asin": asin,
            "is_prime": is_prime,
            "is_best_seller": is_best_seller,
            "bs_category": category,
            "best_seller_info": best_seller_info
        })


    return product_data