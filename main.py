import requests
from bs4 import BeautifulSoup

# import

# soup = BeautifulSoup(html_doc, 'html.parser')


class Property:
    def __init__(self, id: int, type: str, address: str, price: str, description: str):
        self.id = id
        self.type = type
        self.address = address
        self.price = address
        self.description = description
        self.property_url: str = 'https://www.rightmove.co.uk/properties/' + \
            str(self.id)


def rightmove_URL_generator(location: str, sale_or_rent: str = 'sale', include_description: bool = False):
    rightmove_URL = 'https://www.rightmove.co.uk/' + \
        f'property-for-{sale_or_rent}' + '/' + location

    # Add Sorting functionality post link generation. Extract Link + append &sortType=6 (newly listed first)

    html_content = requests.get(rightmove_URL).text
    soup = BeautifulSoup(html_content, 'lxml')

    # print(soup.prettify())  # print the parsed data of html

    # print('Searching for: ' + soup.find(id='searchTitle').text)

    property_list = []

    for property_entry in soup.find_all(class_='l-searchResult is-list'):
        html_id = property_entry.get('id')
        property_id: str = html_id[-html_id.find('-'):]

        property_type: str = property_entry.find(
            class_='propertyCard-title').text.strip()

        property_address: str = property_entry.find(
            class_='propertyCard-address').text.strip()

        property_price: str = property_entry.find(
            class_='propertyCard-priceValue').text.strip()

        property_description: str = property_entry.find(
            class_='propertyCard-description').text.strip()

        property_list.append(Property(id=property_id, type=property_type, address=property_address,
                                      price=property_price, description=property_description))

    print(property_list)


if __name__ == '__main__':
    rightmove_URL_generator(location='Harrow', sale_or_rent='sale')
