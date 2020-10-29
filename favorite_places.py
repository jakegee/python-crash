favorite_places = {
    'paul': [ 'japan', 'paradise', 'okinawa' ],
    'jim': [ 'potato' ],
    'lex': [ 'maldives', 'norilsk' ]
}

for name, places in favorite_places.items():
    print(f"{name} loves to go to")
    for place in places:
        print(f"\t{place}")