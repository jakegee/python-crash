prompt = "Enter your favorite pizza toppings "
prompt += "Loser!"

while True:
    topping = input(prompt)

    if topping == 'quit':
        break
    else:
        print(f"Boy that {topping} sure sounds delicious!")