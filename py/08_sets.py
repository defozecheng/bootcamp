# Sets Operation

# fruits = {"apple","banana","orange"}
# numbers = {1,2,3,4,5}

# # Set operations
# fruits.add("grape")             # Add elementt
# fruits.remove("banana")         # Remove element
# fruits.discard("kiwi")          # Remove if exist (no eror)

# numbers.add(6)
# numbers.remove(3)
# numbers. discard(2)

# print(fruits)
# print(numbers)

# Sets mathematic operation
# sets1 = {1,2,3,4}
# sets2 = {3,4,5,6}

# print(sets1.union(sets2))         # {1,2,3,4,5,6}
# print(sets1.intersection(sets2))  # {3,4}
# print(sets1.difference(sets2))    # {1,2}

# Exercise: Create a system that stores student grades as tuples (name, subject, grade) and uses sets to find unique subjects and students.

grades = [  ("Alice", "Math", 85),  ("Bob", "Science", 92),  ("Alice", "Science", 78),  ("Charlie", "Math", 90),  ("Bob", "Math", 88),  ("Alice", "English", 95) ]

names = set()

for grade in grades:
    names.add(grade[0])

subjects = set()

for grade in grades:
    subjects.add(grade[1])

print(names)
print(subjects)