import json
import os
from datetime import date
from decimal import Decimal
from re import search, sub

import requests
from bs4 import BeautifulSoup

date_today = '2021-01-06'
# date_today = date.today()


def property_avg_price_sold_by_location(location: str):
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


def generate_rightmove_property_dict(location: str, property_type: str = '', sort_by_newest_listed: bool = True, sale_or_rent: str = 'sale'):
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

    properties_dict = dict()

    for property_entry in soup.find_all(class_='l-searchResult is-list'):
        html_id = property_entry.get('id')
        property_id: str = html_id[html_id.find('-')+1:]

        properties_dict[property_id] = {
            'html_id': html_id,
            'property_id': property_id,
            'type': property_entry.find(
                class_='propertyCard-title').text.strip(),
            'address': property_entry.find(
                class_='propertyCard-address').text.strip(),
            f'price_{str(date_today)}': float(sub(r'[^\d.]', '', property_entry.find(
                class_='propertyCard-priceValue').text.strip())),
            'description': property_entry.find(
                class_='propertyCard-description').text.strip(),
            'branch_summary': property_entry.find(
                class_='propertyCard-branchSummary').text.strip(),
            'Avg Price by location': property_avg_price_sold_by_location(
                location=property_entry.find(
                    class_='propertyCard-address').text.strip())
        }
    print(properties_dict)
    return 'hi'
    # return properties_dict


def append_to_property_list_json(location, property_type, sale_or_rent, property_list_filepath_json='Property_temp_file.json'):
    if not os.path.exists(property_list_filepath_json) and property_list_filepath_json.lower().endswith('.json'):
        print('Creating new json')

        property_list_dict_temp = generate_rightmove_property_dict(
            location=location, property_type=property_type, sort_by_newest_listed=True, sale_or_rent=sale_or_rent)

        with open(property_list_filepath_json, 'w') as fp:
            json.dump(property_list_dict_temp, fp)
    else:
        print(f'Appending column with {date_today} prices')

    with open(property_list_filepath_json) as json_file:
        property_list_data = json.load(json_file)

    key_list = []
    for html_id, property_data in property_list_data.items():
        for key in property_data:
            key_list.append(key)

    key_set = set(key_list)

    if any(str(date_today) in column_name for column_name in column_name_list):
        exit(
            f'Prices for {date_today} already exist in the Property Price List.')

    # for html_id, property_data in property_list_data.items():


# TODO
    # 3 cases:
    #     1) property exists + property new => update is fine (would append the new key?)
    #     2) property exists + NONE => property exists unchanged
    #     3) None + property new => update is fine property new

    # # temp_df = pd.DataFrame([n.as_dict() for n in rightmove_property_list])

    # print(temp_combined_df)

    temp_new_values_dict = generate_rightmove_property_dict(
        location=location, property_type=property_type, sort_by_newest_listed=True, sale_or_rent=sale_or_rent)

    # # temp_combined_df.row['Type'].update(temp_combined_df.row['Type_temp'])
    # temp_combined_df['COL3'] = temp_combined_df.Type.combine_first(
    #     temp_combined_df.Type_temp)

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
    # combined_df = temp_combined_df

    # print(combined_df)

    # writer = pd.ExcelWriter(property_list_filepath_json, engine='xlsxwriter', options={
    #     'strings_to_numbers': True})
    # combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
    # writer.save()


if __name__ == '__main__':
    append_to_property_list_json(
        property_list_filepath_json='/Users/virensamani/Projects/RealEstateTool/Property Price List.json',
        location='Harrow',
        property_type='house',
        sale_or_rent='sale')

    # Print Function
    # for n in range(0, len(rightmove_property_list)):
    #     rightmove_property_list[n].print_details()
    #     print('\n')
    # append_to_property_list_json (    #     property_list_filepath_json=r"/Users/virensamani/Projects/RealEstateTool/Property Price List.xlsx")
