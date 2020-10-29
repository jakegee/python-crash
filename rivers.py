rivers = { 'egypt': 'nile', 'brazil': 'amazon', 'mississippi': 'mississippi' }

for values in rivers.values():
    if values == 'nile':
        print(f"{values} is in egypt land")
    elif values == 'amazon':
        print(f"{values} is in brazil nut")
    elif values == 'mississippi':
        print(f"{values} is in the mississippi lol")

for key, value in rivers.items():
    print(key)
for values in rivers.values():
    print(values)