# Create Tuple
numbers = (10, 20, 30, 10)
print(numbers)

# Access Elements
print(numbers[0])
print(numbers[-1])

# Slicing
print(numbers[1:3])

# Count & Index
print(numbers.count(10))
print(numbers.index(30))

# Tuple concatenation
new_tuple = numbers + (40, 50)
print(new_tuple)

# Tuple repetition
print(numbers * 2)

# Single element tuple
single = (5,)
print(type(single))  # tuple

# Tuple Unpacking
a, b, c, d = numbers
print(a, b, c, d)
