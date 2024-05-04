#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# Catch-all unpack 
# ------------------------------------------------------------------------------

car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]

car_ages_descending = sorted(car_ages, reverse=True)

# Use catch-all unpack
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)


# Use catch-all unpack
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)


# Use catch-all unpack
*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)


# ------------------------------------------------------------------------------
# but cannot Catch-all unpack by 1 element 
# ------------------------------------------------------------------------------

# SyntaxError
*others = car_ages_descending

# This will not compile
source = """*others = car_ages_descending"""
eval(source)


# ------------------------------------------------------------------------------
# nested catch-all unpack
# ------------------------------------------------------------------------------

car_inventory = {
	'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
	'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}

((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()

print(f'Best at {loc1} is {best1}, {len(rest1)} others')
print(f'Best at {loc2} is {best2}, {len(rest2)} others')


# ------------------------------------------------------------------------------
# * --> list instance
# if empty, empty list
# ------------------------------------------------------------------------------

short_list = [1, 2]

first, second, *rest = short_list

print(first, second, rest)


# ------------------------------------------------------------------------------
# unpack iterator
# ------------------------------------------------------------------------------

it = iter(range(1, 3))

first, second = it

print(f'{first} and {second}')


# ------------------------------------------------------------------------------
# unpack iterator
# ------------------------------------------------------------------------------

def generate_csv():
	yield ('Date', 'Make' , 'Model', 'Year', 'Price')
	for i in range(100):
		yield ('2019-03-25', 'Honda', 'Fit' , '2010', '$3400')
		yield ('2019-03-26', 'Ford', 'F150' , '2008', '$2400')


all_csv_rows = list(generate_csv())
header = all_csv_rows[0]
rows = all_csv_rows[1:]

print('CSV Header:', header)
print('Row count: ', len(rows))


# Simplified and Clear !!
# NOTE: * comes with list, care about memory consumption

it = generate_csv()
header, *rows = it
print('CSV Header:', header)
print('Row count: ', len(rows))

