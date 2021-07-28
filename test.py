# a = "property-106507469"
# b = "property-80282712"

# print()
# print(b.find('-'))

# print(len(a))
# print(len(b))


# print(a[a.find('-')+1:])

from datetime import date

date_today = str(date.today())
date_today = str('2021-07-2')

column_name_list = ['ID', 'Type', 'Address', 'URL', 'Avg Price by location', 'Price_2021-07-21', 'Price_2021-07-22', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp',
                    'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp',
                    'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp', 'Price_2021-07-22_temp']

print(date_today)

print(any(date_today in column_name for column_name in column_name_list))
