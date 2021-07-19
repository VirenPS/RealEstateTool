import requests
from bs4 import BeautifulSoup

# import

# soup = BeautifulSoup(html_doc, 'html.parser')


class Property:
    def __init__(self, id: int, type: str, address: str, price: str, description: str, branch_summary: str):
        self.id = id
        self.type = type
        self.address = address
        self.price = price
        self.description = description
        self.branch_summary = branch_summary
        self.url: str = 'https://www.rightmove.co.uk/properties/' + \
            str(self.id)

    def print_details(self, include_description: bool = False, include_branch_summary: bool = False):
        print('Type:', self.type)
        print('Address:', self.address)
        print('Price:', self.price)
        if include_description:
            print('Description:', self.description)
        if include_branch_summary:
            print('Description:', self.description)
        print('URL:', self.url)


def generate_rightmove_property_list(location: str, sale_or_rent: str = 'sale'):
    rightmove_URL = 'https://www.rightmove.co.uk/' + \
        f'property-for-{sale_or_rent}' + '/' + location

    # Add Sorting functionality post link generation. Extract Link + append &sortType=6 (newly listed first)

    html_content = requests.get(rightmove_URL).text
    soup = BeautifulSoup(html_content, 'lxml')

    # print(soup.prettify())  # print the parsed data of html

    # print('Searching for: ' + soup.find(id='searchTitle').text)

    property_list: Property = []

    for property_entry in soup.find_all(class_='l-searchResult is-list'):
        html_id = property_entry.get('id')
        property_id: str = html_id[-(html_id.find('-')+1):]
        property_list.append(
            Property(
                id=property_id,
                type=property_entry.find(
                    class_='propertyCard-title').text.strip(),
                address=property_entry.find(
                    class_='propertyCard-address').text.strip(),
                price=property_entry.find(
                    class_='propertyCard-priceValue').text.strip(),
                description=property_entry.find(
                    class_='propertyCard-description').text.strip(),
                branch_summary=property_entry.find(
                    class_='propertyCard-branchSummary').text.strip()

            ))

    return property_list


if __name__ == '__main__':
    rightmove_property_list = generate_rightmove_property_list(
        location='Harrow', sale_or_rent='sale')
    for i in range(0, 5):
        rightmove_property_list[i].print_details()
