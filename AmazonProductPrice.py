import re
from urllib.parse import urlparse
import AmazonProductImages as AmPI
import vars as v

def is_valid_size(value, valid_sizes):
    try:
        # Check if the value is a number or in the valid sizes list
        return float(value) or value in valid_sizes
    except ValueError:
        return False



def get_product_price(soup):
    # Regular expression for matching prices
    price_pattern = re.compile(r'(\d[\d,]*)\.?\d{0,2}')

    # Example: Extracting from a specific attribute
    price_attribute = soup.find("span", {"data-price": True})
    if price_attribute:
        match = price_pattern.search(price_attribute["data-price"])
        if match:
            return match.group()

    # Extracting price from the provided HTML structure
    price_element = soup.find("td", class_="a-color-secondary", string="Price:")
    if price_element:
        price_range_span = price_element.find_next("span", class_="a-price-range")
        if price_range_span:
            prices = [match.group() for match in price_pattern.finditer(price_range_span.text)]
            if prices:
                return prices[-1]  # Return the last price in the range

    # If no price is found, check for another common structure
    price_span = soup.find("span", class_="a-offscreen")
    if price_span:
        match = price_pattern.search(price_span.text)
        if match:
            return match.group()

    # Example: Extracting from a class containing price information
    price_class = soup.find("span", class_=re.compile("price"))
    if price_class:
        match = price_pattern.search(price_class.get_text())
        if match:
            return match.group()

    return "Price information not available"


def extract_price_from_element(price_element):
    # Check if the price is in the "a-offscreen" span
    offscreen_span = price_element.find("span", class_="a-offscreen")
    if offscreen_span:
        return offscreen_span.text.strip()

    # Check if the price is in a nested span structure
    nested_span = price_element.find("span", class_="a-price-whole")
    if nested_span:
        symbol = price_element.find("span", class_="a-price-symbol").text.strip()
        whole = nested_span.text.strip()
        fraction = price_element.find("span", class_="a-price-fraction").text.strip()
        return f"{symbol}{whole}.{fraction}"

    # Check if the price is in a different structure
    price_text = price_element.text.strip()

    # Check for savings percentage structure
    savings_percentage_span = price_element.find("span", class_="savingsPercentage")
    if savings_percentage_span:
        # Extract the savings percentage and adjust the price accordingly
        savings_percentage = savings_percentage_span.text.strip().replace('%', '')
        original_price_match = re.search(r'(\d[\d,]*)\.?\d{0,2}', price_text)
        if original_price_match:
            original_price = original_price_match.group()
            return calculate_discounted_price(original_price, savings_percentage)

    # If none of the above structures match, use the regular expression
    match = re.search(r'(\d[\d,]*)\.?\d{0,2}', price_text)
    if match:
        return match.group()

    return "Price information not available"

def calculate_discounted_price(original_price, savings_percentage):
    try:
        original_price = float(original_price.replace(',', ''))
        savings_percentage = float(savings_percentage)
        discounted_price = original_price - (original_price * (savings_percentage / 100))
        return f"{discounted_price:.2f}"
    except ValueError:
        return "Price information not available"


def extract_size_chart(soup):
    size_chart_div = soup.find("div", {"id": "fit-sizechartv2-0"})
    if size_chart_div:
        size_chart_data = {}

        size_chart_data["title"] = size_chart_div.find("span", {"class": "a-size-base"}).text.strip()

        size_chart_table = size_chart_div.find("table")
        if size_chart_table:
            headers = [th.text.strip() for th in size_chart_table.find_all("th")]
            size_chart_data["headers"] = headers

            rows = []
            for row in size_chart_table.find_all("tr")[1:]:
                # Remove '\xa0' from each cell in the row
                cells = [cell.replace('\xa0', '') for cell in row.stripped_strings]

                # Initialize the cells variable before the loop
                cells = [f"{cells[i]} - {cells[i + 2]}" if i + 2 < len(cells) and cells[i + 1] == '-' else cells[i] for
                         i in range(0, len(cells), 3)]

                rows.append(cells)

            size_chart_data["data"] = rows

        return size_chart_data


def print_extracted_data(soup):
    product_data = {}
    # Extract size chart
    size_chart = extract_size_chart(soup)
    product_data['Size Chart'] = size_chart

    # Get product price
    price = get_product_price(soup)
    product_data['Product Price'] = price

    # Extract and print the number of colors and their titles
    colors_list = soup.find("ul", class_="swatches")
    colors = []
    img_src_list = []
    modified_img_src_list = []

    if colors_list:
        color_items = colors_list.find_all("li", class_=["swatchSelect", "swatchAvailable"])
        num_colors = len(color_items)

        for color_index, color_item in enumerate(color_items):
            color_title = color_item.get("title", "").replace("Click to select ", "")
            img_src = color_item.find("img", class_="imgSwatch")["src"] if color_item.find("img", class_="imgSwatch") else "Image not available"
            modified_img_src = AmPI.modify_image_size([img_src], size=1500)[0]


            # Append to lists
            colors.append(color_title)
            img_src_list.append(img_src)
            modified_img_src_list.append(modified_img_src)


        product_data['Number of Colors'] = num_colors
        product_data['Colors'] = colors
        product_data['Image Src List'] = img_src_list
        product_data['Modified Image Src List'] = modified_img_src_list





    # Extract sizes and prices from twister-plus-inline-twister-container
    inline_twister_container = soup.find("div", {"id": "twister-plus-inline-twister-container"})
    available_sizes = []
    # Sizes list to compare against
    valid_sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']

    if inline_twister_container:
        sizes = inline_twister_container.find_all("span", class_="a-size-base swatch-title-text-display swatch-title-text")
        for size in sizes:
            size_text = size.text.strip()

            # Check if the size is valid
            if is_valid_size(size_text, valid_sizes):
                available_sizes.append(size_text)

        product_data['Sizes'] = available_sizes

    # print(product_data)
    return product_data
