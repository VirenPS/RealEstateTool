import re

import requests
from bs4 import BeautifulSoup


def property_sold_price_lookup_by_location(location: str):
    sold_property_url = 'https://www.rightmove.co.uk/house-prices/search.html?searchLocation=' + location
    print("'" + sold_property_url + "'")

    sold_property_html_content = requests.get(sold_property_url).text
    sold_property_soup = BeautifulSoup(
        sold_property_html_content, 'lxml')

    try:
        avg_property_price_summary = sold_property_soup.find(
            'meta', attrs={'name': 'description'})['content']

        avg_property_price = re.search(
            'is.* over', avg_property_price_summary).group(0)[3:-5]

        return avg_property_price
    except Exception as e:
        # Need to clean. Seperate Attribute and NoneType exceptions.
        return('Unavailable')


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

    def print_details(self, include_description: bool = False, include_branch_summary: bool = True):
        print('Type:', self.type)
        print('Address:', self.address)
        print('Price:', self.price)
        if include_branch_summary:
            print('Branch Summary:', self.branch_summary)
        print('URL:', self.url)
        print('+ Average price by location:', property_sold_price_lookup_by_location(
            location=self.address))
        if include_description:
            print('Description:', self.description)

    def append_to_sheet(self):
        pass


def generate_rightmove_property_list(location: str, property_type: str = '', sort_by_newest_listed: bool = True, sale_or_rent: str = 'sale'):
    rightmove_URL = 'https://www.rightmove.co.uk/' + \
        f'property-for-{sale_or_rent}' + '/' + location + '?'

    if sort_by_newest_listed:
        rightmove_URL += '&sortType=6'

    if property_type == 'house':
        rightmove_URL += '&propertyTypes=detached%2Cpark-home%2Csemi-detached%2Cterraced'
    elif property_type == 'flat':
        rightmove_URL += '&propertyTypes=flat'

    # Add Sorting functionality post link generation. Extract Link + append &sortType=6 (newly listed first)

    html_content = requests.get(rightmove_URL).text
    soup = BeautifulSoup(html_content, 'lxml')

    # print(soup.prettify())  # print the parsed data of html

    # print('Searching for: ' + soup.find(id='searchTitle').text)

    property_list: Property = []

    for property_entry in soup.find_all(class_='l-searchResult is-list'):
        html_id = property_entry.get('id')

        property_id: str = html_id[html_id.find('-')+1:]
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
    # rightmove_property_list = generate_rightmove_property_list(
    #     location='Harrow', property_type='house', sale_or_rent='sale')

    # for n in range(0, len(rightmove_property_list)):
    #     rightmove_property_list[n].print_details()
    #     print('\n')
