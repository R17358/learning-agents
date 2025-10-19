# Create List
fruits = ["apple", "banana", "cherry", "apple"]
print(fruits)

# Access Elements
print(fruits[0])       # first element
print(fruits[-1])      # last element
print(fruits[1:3])     # slicing

# Modify
fruits[1] = "mango"
print(fruits)

# Add Elements
fruits.append("orange")
fruits.insert(2, "grapes")
print(fruits)

# Extend another list
more_fruits = ["kiwi", "melon"]
fruits.extend(more_fruits)
print(fruits)

# Remove Elements
fruits.remove("apple")    # removes first occurrence
popped = fruits.pop(1)    # remove by index
del fruits[0]             # delete by index
print(fruits)

# Count and Index
print(fruits.count("apple"))
print(fruits.index("grapes"))

# Sort and Reverse
fruits.sort()
print("Sorted:", fruits)
fruits.reverse()
print("Reversed:", fruits)

# Copy
new_list = fruits.copy()
print("Copied:", new_list)

# Clear
fruits.clear()
print("Cleared:", fruits)
