import os
from datetime import date
from decimal import Decimal
from re import search, sub

import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook

date_today = '2021-01-04'
# date_today = date.today()


def property_sold_price_lookup_by_location(location: str):
    sold_property_url = 'https://www.rightmove.co.uk/house-prices/search.html?searchLocation=' + location
    # print("'" + sold_property_url + "'")

    sold_property_html_content = requests.get(sold_property_url).text
    sold_property_soup = BeautifulSoup(
        sold_property_html_content, 'lxml')

    try:
        avg_property_price_summary = sold_property_soup.find(
            'meta', attrs={'name': 'description'})['content']

        avg_property_price = search(
            ' is.* over ', avg_property_price_summary).group(0)[4:-6]

        return avg_property_price
    except Exception as e:
        # Need to clean. Seperate Attribute and NoneType exceptions.
        return('Unavailable')


class Property:
    def __init__(self, id: int, type: str, address: str, price: int, description: str, branch_summary: str):
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

    def as_dict(self):
        return {'ID': self.id, 'Type': self.type, 'Address': self.address, 'URL': self.url,
                'Avg Price by location': property_sold_price_lookup_by_location(location=self.address), f'Price_{date_today}': self.price}


def append_to_dataframe(property_list_path='Property_temp_file.xlsx'):
    if not os.path.exists(property_list_path):
        print('Creating new Dataframe')
        df = pd.DataFrame([n.as_dict() for n in rightmove_property_list])
        writer = pd.ExcelWriter(r'/Users/virensamani/Projects/RealEstateTool/Property Price List.xlsx', engine='xlsxwriter', options={
            'strings_to_numbers': True})
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
    else:
        print(f'Appending column with {date_today} prices')

        prices_ws = load_workbook(property_list_path)['Sheet1']
        prices_df = pd.DataFrame(prices_ws.values)

        new_header = prices_df.iloc[0]
        prices_df = prices_df[1:]
        prices_df.columns = new_header

        column_name_list = list(prices_df.columns.values)

        if any(str(date_today) in column_name for column_name in column_name_list):
            exit(
                f'Prices for {date_today} already exist in the Property Price List.')

        temp_df = pd.DataFrame([n.as_dict() for n in rightmove_property_list])

        for index, row in prices_df.iterrows():
            row['ID'] = float(row['ID'])

        for index, row in temp_df.iterrows():
            row['ID'] = float(row['ID'])

        temp_combined_df = prices_df.join(temp_df.set_index(
            'ID'), on='ID', rsuffix='_temp', how='outer')

        # temp_combined_df.row['Type'].update(temp_combined_df.row['Type_temp'])
        temp_combined_df['COL3'] = temp_combined_df.Type.combine_first(
            temp_combined_df.Type_temp)

        # Update Values
        # for index, row in temp_combined_df.iterrows():
        # print('_______')
        # df.Col2 = df.Col1.where(df.Col2 > 'X', df.Col2)
        # if len(str(row['Type'])) < len(str(row['Type_temp'])):
        #     row['Type'] = row['Type_temp']
        # if len(str(row['Address'])) < len(str(row['Address_temp'])):
        #     row['Address'] = row['Address_temp']
        # if len(str(row['URL'])) < len(str(row['URL_temp'])):
        #     row['URL'] = row['URL_temp']
        # if len(str(row['Avg Price by location'])) < len(str(row['Avg Price by location_temp'])):
        #     row['Avg Price by location'] = row['Avg Price by location_temp']
        # temp_combined_df.drop([f'Type_{date_today}_temp', 'Address_temp', 'URL_temp',
        #                   'Avg Price by location_temp'], inplace=True, axis=1)

        # print(temp_combined_df)

        # combined_df = temp_combined_df.loc[:, [
        #     '_temp' not in i for i in temp_combined_df.columns]]
        combined_df = temp_combined_df

        # print(combined_df)

        writer = pd.ExcelWriter(property_list_path, engine='xlsxwriter', options={
            'strings_to_numbers': True})
        combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()


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
                price=Decimal(sub(r'[^\d.]', '', property_entry.find(
                    class_='propertyCard-priceValue').text.strip())),
                description=property_entry.find(
                    class_='propertyCard-description').text.strip(),
                branch_summary=property_entry.find(
                    class_='propertyCard-branchSummary').text.strip()

            ))

    return property_list


def append_to_property_list(property_list_csv_path):
    df = pd.DataFrame([n.as_dict() for n in rightmove_property_list])
    df.to_csv(
        r'/Users/virensamani/Projects/RealEstateTool/property_prices.csv', index=False)


if __name__ == '__main__':
    rightmove_property_list = generate_rightmove_property_list(
        location='Harrow', property_type='house', sale_or_rent='sale')

    # Print Function
    # for n in range(0, len(rightmove_property_list)):
    #     rightmove_property_list[n].print_details()
    #     print('\n')
    append_to_dataframe(
        property_list_path=r"/Users/virensamani/Projects/RealEstateTool/Property Price List.xlsx")
