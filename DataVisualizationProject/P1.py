dict={'one':{'firstname':'sumana'},
      'two':{'firstname':'kavana'}}

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

print(dict.keys())
for data in dict:
      print(dict[data].keys())

s = '3.00'
print(s.isdecimal(), " ", s.isnumeric(), " ", s.isdigit(), " ", isfloat(s))

# contains alphabets
s = "32ladk3"
print(s.isdecimal())

# contains alphabets and spaces
s = "Mo3 nicaG el l22er"
print(s.isdecimal())

