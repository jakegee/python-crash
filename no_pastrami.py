sandwich_orders = [ 'pastrami', 'potato', 'pastrami', 'bigbean', 'fakeflavor', 'rye', 'pastrami' ]
finished_sandwiches = []

prompt = "the deli has run out of pastrami"
print(prompt)

while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')

for sandwich in sandwich_orders:
    print(f"{sandwich}")