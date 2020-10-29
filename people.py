friend_0 = {}
friend_1 = {}
friend_2 = {}

friend_0['first'] = 'john'
friend_0['last'] = 'paul'
friend_0['city'] = 'eh'
friend_0['state'] = 'nj'
friend_0['age'] = 18

friend_1['first'] = 'chris'
friend_1['last'] = 'katan'
friend_1['city'] = 'la'
friend_1['state'] = 'ca'
friend_1['age'] = 65

friend_2['first'] = 'tim'
friend_2['last'] = 'robbins'
friend_2['city'] = 'seattle'
friend_2['state'] = 'wa'
friend_2['age'] = 42

people = [ friend_0, friend_1, friend_2 ]

for persons in people:
    print(persons)