import AllProductDetails as APD
import pandas as pd
import AmazonPagesNumber as PN
import StorePage as SP
import InsertIntoDB as DB
import vars as v
from urllib.parse import urlparse

def scrape_amazon_search(url):
    data = []

    # Get the last page number using the URL
    last_page_number = PN.get_last_page_number(url)


    for page in range(1, last_page_number + 1):
        current_url = f"{url}&page={page}"
        page_data = SP.scrape_page(current_url)

        for item in page_data:
            asin = item.get("data-asin")
            price_element = item.get("price_element")
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
                title, rating, availability, image_sources, category, sold_count, about_points = APD.scrape_product_details(product_link)

                # Fetch product price for the current product link
                if isinstance(price_element, str):
                    price = price_element.strip().replace('\xa0', ' ')
                else:
                    price = price_element.get_text().strip().replace('\xa0', ' ')

                # Prime check
                prime_status = "Amazon Prime" if is_prime else "Not Prime"
                # Score Check
                sold_count = sold_count if sold_count else "Score Not Found"
                # About Check
                about_points = about_points if about_points else "About this item section not found."
                # Best Seller Check
                is_best_seller = "Best Seller" if is_best_seller else "---"



                product_data = {
                    "Product Title": title,
                    "Product category": category,
                    "Product Price": price,
                    "Prime Status": prime_status,
                    "Product Score": sold_count,
                    "Best Seller Status": is_best_seller,
                    "Best Seller Category": bs_category,
                    "Best Seller Info": best_seller_info,
                    "Rating": rating,
                    "Product Description": about_points,
                    "Product availability": availability,
                    "Product Link": product_link,
                    "Image Sources": image_sources
                }

                data.append(product_data)


                # Print the result
                print("Product Title:", title)
                print("Product Category:", category)
                print("Product Price:", price)
                print("Prime Status:", prime_status)
                print("Product Score:", sold_count)
                print("Best Seller Status:", is_best_seller)
                print("Best Seller Category:", bs_category)
                print("Best Seller Info:", best_seller_info)
                print("Rating:", rating)
                print("Product Description:", about_points)
                print("Product availability:", availability)
                print("Product Link:", product_link)
                print("Image Sources:", image_sources)
                print("\n" + "=" * 50 + "\n")

                # Function call to insert into the database
                # DB.insert_into_db(title, price, rating, product_link, about_points, image_sources, category, sold_count, availability)

    df = pd.DataFrame(data)
    df.to_csv(v.csv_filename, index=False)