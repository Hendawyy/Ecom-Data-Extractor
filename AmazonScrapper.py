from requests import RequestException

import AllProductDetails as APD
import pandas as pd
import AmazonPagesNumber as PN
import StorePage as SP
import InsertIntoDB as DB
import vars as v
from urllib.parse import urlparse
import PrintProductDetails as PPD

def scrape_amazon_search(url):
    data = []

    # Get the last page number using the URL
    last_page_number = PN.get_last_page_number(url)

    for page in range(1, last_page_number + 1):
        current_url = f"{url}&page={page}"
        try:
            page_data = SP.scrape_page(current_url)

            for item in page_data:
                asin = item.get("data-asin")
                is_prime = item.get("is_prime")
                is_best_seller = item.get("is_best_seller")
                bs_category = item.get("bs_category")
                best_seller_info = item.get("best_seller_info")
                if asin:
                    # Extract domain from the provided URL
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc.split('.')[-1]
                    # Construct dynamic product link based on the domain
                    product_link = f"https://amazon.{domain}/-/en/dp/{asin}"

                    # Fetch product details for the current product link
                    title, rating, availability, image_sources, category, sold_count, about_points, price = APD.scrape_product_details(product_link)

                    # Prime check
                    prime_status = "Amazon Prime" if is_prime else "Not Prime"
                    # Score Check
                    sold_count = sold_count if sold_count else "Score Not Found"
                    # About Check
                    about_points = about_points if about_points else "About this item section not found."
                    # Best Seller Check
                    is_best_seller = "Best Seller" if is_best_seller else "---"

                    product_data = {
                        "Product ASIN": asin,
                        "Product Title": title,
                        "Product category": category,
                        "Product Price": price.get('Product Price', []),
                        "Prime Status": prime_status,
                        "Product Score": sold_count,
                        "Best Seller Status": is_best_seller,
                        "Best Seller Category": bs_category,
                        "Best Seller Info": best_seller_info,
                        "Rating": rating,
                        "Product Description": about_points,
                        "Product availability": availability,
                        "Product Link": product_link,
                        "Image Sources": image_sources,
                        "Number of Colors": price.get('Number of Colors', []),
                        "Colors": price.get('Colors', []),
                        "Colored Img Src": price.get('Image Src List', []),
                        "Colored Img Src Modified": price.get('Modified Image Src List', []),
                        "Size Chart": price.get('Size Chart', []),
                        "Sizes": price.get('Sizes', [])
                    }
                    data.append(product_data)
                    PPD.print_product_details(product_data)
                    # Function call to insert into the database
                    # DB.insert_into_db(title, price, rating, product_link, about_points, image_sources, category, sold_count, availability)
        except RequestException as e:
            print(f"RequestException: {e}")
            print(f"Failed URL: {current_url}")
            print("Maximum retries reached. Request failed.")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

    df = pd.DataFrame(data)
    df.to_csv(v.csv_filename+'.csv', index=False)

