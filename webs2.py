import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://tonaton.com/c_electronics'


def get_pagination_url():
    links = []
    new_link = 'https://tonaton.com/c_electronics?page=2'
    for j in range(2, 499):
        temp_link = new_link[0:len(new_link) - 1]
        new_link = temp_link + f'{j}'

        links.append(new_link)

    return links


def scrape_pages(link):

    with open(f'scrapped_file.csv', 'a', encoding='utf-8') as f:

        # fieldnames = ['Name', 'Price', 'Region', 'City', 'Usage', 'Image']

        csv_writer = csv.writer(f)

        # if not fieldnamesWritten:
        #     csv_writer.writerow(fieldnames)
        #     fieldnamesWritten = True

        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        data = soup.find_all('div', class_="product__container flex")

        for other_data in data:
            product_container = other_data.find_all('a', class_='product__item flex')
            product_usage = ''
            for new_data in product_container:
                product_image_tag = new_data.find('div', class_='product__image')
                image_div = product_image_tag.find('img')
                image_src = str(image_div.get('src'))  # src was replaced

                product_info = new_data.find('div', class_='product__content')
                product_price = product_info.find('span', class_='product__title').text.strip()
                # product_price = product_price.replace(',', '')
                # product_price = int(product_price[4:])
                product_description = new_data.find('p', class_='product__description').text.strip()
                product_location = new_data.find('p', class_='product__location').text.split(',')
                if len(product_location) >= 2:
                    product_region = product_location[0].strip()
                    product_city = product_location[1].strip()
                else:
                    pass
                product_usage_tag = new_data.find('div', class_='product__tags flex wrap').span
                if product_usage_tag:
                    product_usage = product_usage_tag.text.strip()
                else:
                    pass

                if product_usage.startswith('Brand') or product_usage.startswith('Used'):
                    info = [product_description, product_price, product_region, product_city, product_usage, image_src]
                    csv_writer.writerow(info)
                else:
                    pass


def get_info():
    df = pd.read_csv('scrapped_file.csv')
    return df.describe().loc['mean']


if __name__ == '__main__':
    with open('scrapped_file.csv', 'w') as file:
        fieldnames = ['Name', 'Price', 'Region', 'City', 'Usage', 'Image']
        csv_write = csv.writer(file)
        csv_write.writerow(fieldnames)

    pagination_links = get_pagination_url()
    for pagination_link in pagination_links:
        scrape_pages(pagination_link)
        print('successfully saved')
    average = get_info()
    print(f'The average price of an item is {average}')

