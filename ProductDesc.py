from bs4 import BeautifulSoup
import vars as v

def get_about_this_item(soup):

    # Find the "About this item" section by searching for the text
    about_section = soup.find('h1', string=lambda text: text and 'About this item' in text)

    if about_section:
        # Find the nearest ul element after the "About this item" section
        ul_element = about_section.find_next('ul', class_='a-unordered-list')


        if ul_element:
            # Extract the text from each span with class 'a-list-item' within li elements
            points = [li.span.text.strip() for li in ul_element.find_all('li', class_='a-spacing-mini')]

            return points

    return None


