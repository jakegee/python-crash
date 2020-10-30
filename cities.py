cities = {
    'tokyo': {
        'country': 'japan',
        'population': '10',
        'fact': 'i dunno',
    },
    'nyc': {
        'country': 'usa',
        'population': '20',
        'fact': 'easily largest city in the world',
    },
    'london': {
        'country': 'england',
        'population': 'a million',
        'fact': 'tiniest city in the world',
    },
}

for key, value in cities.items():
    print(f"key {key}")
    city_stuff = f"{value['country']} {value['population']} {value['fact']}"
    print(f"\t{city_stuff}")
