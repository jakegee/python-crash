dinner_guests = [ 'tom', 'dick', 'harry' ]
print(f"\nhey {dinner_guests[0].title()} welcome to dinner") 

guest_cancelation = 'harry'
print(f"uh oh {guest_cancelation.title()} can't make it")
dinner_guests.remove('harry')
dinner_guests.append('richard')
print(f"this is my new dinner guest then {dinner_guests[2].title()}")

print("as it turns out we have more space at the table")
dinner_guests.insert(0, 'christian')
dinner_guests.insert(2, 'jasmine')
dinner_guests.append('johnica')
print(dinner_guests)

print("i can only invite two guests now, sorry folks")
uninvited_guest = dinner_guests.pop()
print(f"sorry i can't invite you {uninvited_guest}")
uninvited_guest = dinner_guests.pop()
print(f"sorry i can't invite you {uninvited_guest}")
uninvited_guest = dinner_guests.pop()
print(f"sorry i can't invite you {uninvited_guest}")
uninvited_guest = dinner_guests.pop()
print(f"sorry i can't invite you {uninvited_guest}")
print(f"you're still invited {dinner_guests[0]} and {dinner_guests[1]}")

print(len(dinner_guests))
