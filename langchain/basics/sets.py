# Create Set
myset = {1, 2, 3, 4, 2}
print(myset)  # {1, 2, 3, 4}

# Add Elements
myset.add(5)
myset.update([6, 7])
print(myset)

# Remove Elements
myset.remove(2)       # error if not found
myset.discard(10)     # no error if not found
popped = myset.pop()  # removes random element
print("After pop:", myset)

# Set Operations
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print("Union:", A | B)
print("Intersection:", A & B)
print("Difference:", A - B)
print("Symmetric Difference:", A ^ B)

# Membership
print(2 in A)
print(10 not in A)

# Copy and Clear
copy_set = A.copy()
A.clear()
print("Cleared A:", A)
print("Copy of A:", copy_set)
