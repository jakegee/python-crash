sandwich_orders = [ 'pastrami', 'potato', 'bigbean', 'fakeflavor', 'rye' ]
finished_sandwiches = []

while sandwich_orders:
    working_sandwiches = sandwich_orders.pop()
    print(f"i made your {working_sandwiches} stinky sandwich")
    finished_sandwiches.append(working_sandwiches)

for sandwich in finished_sandwiches:
    print(f"{sandwich}")