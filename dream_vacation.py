responses = {}

poll_active = True

while poll_active:
    name = input("What's your name bub?")
    response = input("If you could visit one place in the world, where would you go?")

    responses[name] = response

    repeat = input("Would you like to continue to next person?")
    if repeat == 'no':
        poll_active = False

for name, response in responses.items():
    print(f"{name} wants to go to {response}")
