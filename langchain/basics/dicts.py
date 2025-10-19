# Create Dictionary
student = {
    "name": "Ritesh",
    "age": 22,
    "course": "Data Science"
}
print(student)

# Access Elements
print(student["name"])
print(student.get("age"))
print(student.get("marks", "Not Found"))  # default value if key missing

# Modify
student["age"] = 23
student["college"] = "MIT"
print(student)

# Remove
student.pop("course")         # remove by key
student.popitem()             # removes last item
del student["age"]            # delete by key
print(student)

# Copy
new_dict = student.copy()
print("Copied Dict:", new_dict)

# Keys, Values, Items
print("Keys:", student.keys())
print("Values:", student.values())
print("Items:", student.items())

# Loop through dict
for key, value in student.items():
    print(key, ":", value)

# Clear
student.clear()
print("Cleared:", student)

# Nested Dictionary
students = {
    "s1": {"name": "Ritesh", "marks": 90},
    "s2": {"name": "Aman", "marks": 85}
}
print(students["s1"]["name"])
