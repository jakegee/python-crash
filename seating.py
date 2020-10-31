guests = input("how many guests will be eating tonight? ")
guests = int(guests)

if guests > 8:
    print(f"oof far too many")
else:
    print(f"table for {guests} available")