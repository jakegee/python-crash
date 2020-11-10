prompt = "Yes how old are you my good man? "
age = 0

while True:
    age = int(input(prompt))

    if age < 3:
        print(f"you are {age} which means free time!")
        break
    elif age in range(3, 13):
        print(f"you are {age} so your ticky is $10")
        break
    elif age > 12:
        print(f"you are {age} so your ticky is $15")
        break
    else:
        print("you're not answering the question friendo")
