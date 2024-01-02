import requests
from bs4 import BeautifulSoup


def scrape_image_src(soup):
    img_tags = soup.select('#imageBlock img')
    image_src_list = []

    for img in img_tags:
        if 'src' in img.attrs:
            src = img['src']
            image_src_list.append(src)

    return modify_image_size(image_src_list)

def modify_image_size(image_src_list, size=950):
    modified_image_src_list = []

    for src in image_src_list:
        # Check if size specifications are present in the URL
        if '_AC_US40_' in src:
            # Replace size specifications with the desired size
            src = src.replace('_AC_US40_', f'_AC_US{size}_')
        elif '_SX38_SY50_CR,0,0,38,50_' in src:
            src = src.replace('_SX38_SY50_CR,0,0,38,50_', f'_SX{size}_SY{size}_')
        elif '_AC_SR38,50_' in src:
            # Handle cases with '_AC_SR38,50_' at the end of the URL
            src = src.replace('_AC_SR38,50_', f'_AC_SR{size},{size}_')
        elif '_SS47_' in src or '_SS38,50_' in src:
            # Handle cases with '_SS47_' or '_SS38,50_' at the end of the URL
            src = src.replace('_SS47_', f'_SS900_').replace('_SS38,50_', f'_SS900_')

        # Add the modified URL to the list
        modified_image_src_list.append(src)

    return modified_image_src_list

