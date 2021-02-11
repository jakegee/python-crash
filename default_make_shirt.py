def make_shirt(size='L', text='This is default text'):
    """Text of the shirt goes here"""
    print(f"this is size {size.title()}")
    print(f"{text}")

make_shirt('M')
make_shirt()
make_shirt(size='XL',text='the XL one')