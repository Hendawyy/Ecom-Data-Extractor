import requests
from bs4 import BeautifulSoup


def scrape_image_src(soup):
    img_tags = soup.select('#imageBlock img')
    size = 1500
    image_src_list = []

    for img in img_tags:
        if 'src' in img.attrs:
            src = img['src']

            # Check if size specifications are present in the URL
            if '_AC_US40_' in src:
                # Replace size specifications with the desired size
                src = src.replace('_AC_US40_', f'_AC_US{size}_')
            elif '_SX38_SY50_CR,0,0,38,50_' in src:
                src = src.replace('_SX38_SY50_CR,0,0,38,50_', f'_SX{size}_SY{size}_')
            else:
                # If size specifications are not present, add them based on the image type
                if '/I/' in src:
                    # Main product image
                    src = src.replace('/I/', f'/I/_AC_US{size}_')
                elif '/S/' in src:
                    # Additional images
                    src = src.replace('/S/', f'/S/_AC_US{size}_')

            # Add the modified URL to the list
            image_src_list.append(src)

    return image_src_list
