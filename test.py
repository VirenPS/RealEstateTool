# a = "property-106507469"
# b = "property-80282712"

# print()
# print(b.find('-'))

# print(len(a))
# print(len(b))


# print(a[a.find('-')+1:])

# from datetime import date

# date_today = str(date.today())
# date_today = str('2021-07-2')

# column_name_list = ['ID', 'Type', 'Address', 'URL', 'Avg Price by location', 'Price_2021-07-21', 'Price_2021-07-22', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp',
#                     'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp',
#                     'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp']

# print(date_today)

# print(any(date_today in column_name for column_name in column_name_list))

import json

# property_list_filepath_json = '/Users/virensamani/Projects/RealEstateTool/Property Price List.json'

# with open(property_list_filepath_json) as json_file:
#     property_list_data = json.load(json_file)

# key_list = []
# for html_id, property_data in property_list_data.items():
#     for key in property_data:
#         key_list.append(key)

# print(property_list_data)

a = {'79468356': {'html_id': 'property-79468356',
                  'property_id': '79468356', 'type': '3 bedroom flat for sale'}}
b = {'11111111': {'html_id': 'property-111111',
                  'property_id': '22222', 'type': '5 rooms'}}



c = a.update(b)
print(c)
