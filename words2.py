newwords = {}

newwords['function'] = 'you know its like the whole block of code'
function = newwords['function']
newwords['method'] = 'its like a get on a dict key'
method = newwords['method']
newwords['dunno'] = 'do i really know any new words'
dunno = newwords['dunno']
newwords['sup'] = 'you know its like the whole block of code'
function = newwords['sup']
newwords['nup'] = 'its like a get on a dict key'
method = newwords['nup']
newwords['bup'] = 'do i really know any new words'
dunno = newwords['bup']

for key, value in newwords.items():
    print(f"{key}")
    print(f"{value}")