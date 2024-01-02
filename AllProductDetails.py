from bs4 import BeautifulSoup
import requests
import ProductTitle as PT
import ProductRaiting as PRT
import ProductAvailability as PA
import AmazonProductImages as PI
import ProductCategorey as PC
import ProductScore as PS
import ProductDesc as PD
import vars as v
import ServiceUnavilableHandler as SUH
import AmazonProductPrice as PP

def scrape_product_details(product_link):
    new_webpage = SUH.make_request(product_link, v.HEADERS)
    if new_webpage is None:
        return []
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    title = PT.get_product_title(new_soup)
    rating = PRT.get_product_rating(new_soup)
    availability = PA.get_availability(new_soup)
    image_sources = PI.scrape_image_src(new_soup)
    category = PC.get_product_category(new_soup)
    sold_count = PS.get_product_sold_count(new_soup)
    about_points = PD.get_about_this_item(new_soup)
    price = PP.print_extracted_data(new_soup)

    return title, rating, availability, image_sources, category, sold_count, about_points, price
