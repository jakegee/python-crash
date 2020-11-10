prompt = "Enter your favorite pizza toppings "
prompt += "Loser!: "

active = True

while active:
    topping = input(prompt)

    if topping == 'quit':
        active = False
    else:
        print(f"Boy that {topping} sure sounds delicious!")