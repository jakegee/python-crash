# 4-3
# counting = range(1, 21)
# for numbers in counting:
#     print(numbers)

# 4-5
# numbers = []
# for number in range(1, 1000001):
#     numbers.append(number)

# print(min(numbers))
# print(max(numbers))
# print(sum(numbers))

# 4-6
# odd_numbers = []
# for numbers in range(1, 21, 2):
#     odd_numbers.append(numbers)

# print(odd_numbers)

# 4-7
# multiples_three = []
# for numbers in range(3, 31, 3):
#     multiples_three.append(numbers)

# print(multiples_three)

# 4-8
# cubes = []
# for number in range(1, 11):
#     cubes.append(number**3)

# print(cubes)

cubes = [value**3 for value in range(1,11)]
print(cubes)