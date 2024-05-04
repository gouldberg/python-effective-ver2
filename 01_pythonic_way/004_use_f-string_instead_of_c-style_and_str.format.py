#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# C-style format string and its problem
# ------------------------------------------------------------------------------

a = 0b10111011
b = 0xc5f

print('Binary is %d, hex is %d' % (a, b))


# ----------
key = 'my_var'
value = 1.234

formatted = '%-10s = %.2f' % (key, value)
print(formatted)

# key and value are swapped in order:  TypeError
reordered_tuple = '%-10s = %.2f' % (value, key)

# key and value are swapped in order:  TypeError
reordered_string = '%.2f = %-10s' % (key, value)


# ------------------------------------------------------------------------------
# C-style format string and its problem
# ------------------------------------------------------------------------------

pantry = [
    ('avocados', 1.25),
    ('bananas', 2.5),
    ('cherries', 15),
]

for i, (item, count) in enumerate(pantry):
    print('#%d: %-10s = %.2f' % (i, item, count))


# this format string is long ... 
for i, (item, count) in enumerate(pantry):
    print('#%d: %-10s = %d' % (i + 1, item.title(), round(count)))


# ----------
name = 'Max'
template = '%s loves food. See %s cook.'

# same value multiple times ...
formatted = template % (name, name)
print(formatted)

# same method (.title()) should be added multiple times ...
name = 'brad'
formatted = template % (name.title(), name.title())
print(formatted)


# ------------------------------------------------------------------------------
# C-style format string, formatting by not tuple but dictionary
#  --> no multiple times, no caring order ... but still have problems
# ------------------------------------------------------------------------------

key = 'my_var'
value = 1.234

old_way = '%-10s = %.2f' % (key, value)

new_way = '%(key)-10s = %(value).2f' % {
    'key': key, 'value': value}  # Original

reordered = '%(key)-10s = %(value).2f' % {
    'value': value, 'key': key}  # Swapped

assert old_way == new_way == reordered


# ----------
name = 'Max'

template = '%s loves food. See %s cook.'
before = template % (name, name)   # Tuple

template = '%(name)s loves food. See %(name)s cook.'
after = template % {'name': name}  # Dictionary

assert before == after


# ----------
# but not readable ...
for i, (item, count) in enumerate(pantry):
    before = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))

    after = '#%(loop)d: %(item)-10s = %(count)d' % {
        'loop': i + 1,
        'item': item.title(),
        'count': round(count),
    }

    assert before == after


# ----------
# have to set multiple times ....
soup = 'lentil'
formatted = 'Today\'s soup is %(soup)s.' % {'soup': soup}
print(formatted)


# ----------
# dictionary (menu) and template is separately written ... not readable
menu = {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}

template = ('Today\'s soup is %(soup)s, '
            'buy one get two %(oyster)s oysters, '
            'and our special entrée is %(special)s.')

formatted = template % menu
print(formatted)


# ------------------------------------------------------------------------------
# builtin format
# ------------------------------------------------------------------------------

# ',': 数値を3桁で区切る
a = 1234.5678
formatted = format(a, ',.2f')

print(formatted)


# ----------
# '^': centering
b = 'my string'
formatted = format(b, '^20s')

print('*', formatted, '*')


# ------------------------------------------------------------------------------
# str.format
# ------------------------------------------------------------------------------

key = 'my_var'
value = 1.234

formatted = '{} = {}'.format(key, value)
print(formatted)


# ----------
# can control format
formatted = '{:<10} = {:.2f}'.format(key, value)
print(formatted)


# ----------
# %% is escaping %
print('%.2f%%' % 12.5)

# escaping {}
print('{} replaces {{}}'.format(1.23))


# ----------
# specifying positional index (now 1 for value, 0 for key)
formatted = '{1} = {0}'.format(key, value)
print(formatted)


# ----------
# not required to set name multiple times
formatted = '{0} loves food. See {0} cook.'.format(name)
print(formatted)


# ----------
# but still long and not readable ...
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))

    new_style = '#{}: {:<10s} = {}'.format(
        i + 1,
        item.title(),
        round(count))

    assert old_style == new_style


# ----------
# string conversion
formatted = 'First letter is {menu[oyster][0]!r}'.format(menu=menu)

print(formatted)


# ----------
# old (C-style) and new (str.format)
old_template = (
    'Today\'s soup is %(soup)s, '
    'buy one get two %(oyster)s oysters, '
    'and our special entrée is %(special)s.')

old_formatted = old_template % {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}

new_template = (
    'Today\'s soup is {soup}, '
    'buy one get two {oyster} oysters, '
    'and our special entrée is {special}.')

new_formatted = new_template.format(
    soup='lentil',
    oyster='kumamoto',
    special='schnitzel',
)

assert old_formatted == new_formatted


# ------------------------------------------------------------------------------
# f-string (format string)
# ------------------------------------------------------------------------------

key = 'my_var'
value = 1.234

formatted = f'{key} = {value}'
print(formatted)


# ----------
formatted = f'{key!r:<10} = {value:.2f}'
print(formatted)


# ----------
# f-string is most simple compared to other formats !!
f_string = f'{key:<10} = {value:.2f}'

c_tuple  = '%-10s = %.2f' % (key, value)
str_args = '{:<10} = {:.2f}'.format(key, value)
str_kw   = '{key:<10} = {value:.2f}'.format(key=key, value=value)
c_dict   = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}

assert c_tuple == c_dict == f_string
assert str_args == str_kw == f_string


# ----------
# f-string is most simple compared to other formats !!
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))

    new_style = '#{}: {:<10s} = {}'.format(
        i + 1,
        item.title(),
        round(count))

    f_string = f'#{i+1}: {item.title():<10s} = {round(count)}'

    assert old_style == new_style == f_string


# ----------
# inside {}, python expression can be applied
for i, (item, count) in enumerate(pantry):
    print(f'#{i+1}: '
          f'{item.title():<10s} = '
          f'{round(count)}')


# ----------
# nested {}
places = 3
number = 1.23456
print(f'My number is {number:.{places}f}')

