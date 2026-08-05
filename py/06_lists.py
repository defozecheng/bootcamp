#List: A set of data within square brackets [...]

# fruits = ["apple","banana","orange"]
# numbers = [1,2,3,4,5]
# mixed = ["hello",42,3.14,True]
# empty_list = []

# # Accessing Elements
# print(fruits[0])
# print(fruits[-1])
# print(numbers[1:4])
# print(numbers[:3])
# print(numbers[2:])

# Lists Operation: CRUD a list

# fruits.append("grape")
# fruits.insert(1,"kiwi")
# fruits.remove("banana")
# popped = fruits.pop()
# fruits.sort()
# fruits.reverse()

# # List operations
# len(fruits)
# "apple" in fruits
# fruits + ["mango"]
# fruits * 2

# edited_fruits = fruits.copy()
# edited_fruits.append("grape")

# print(edited_fruits)
# print(len(fruits))
# print(fruits)
# print(popped)

# Exercise 1: Create a grocery list and perform various opetations.

# groceries_list = ["apple","milk","bread","egg"]
# groceries_list.append("chicken")
# groceries_list.insert(1,"orange")
# groceries_list.remove("bread")

# print(groceries_list)

# Exercise 2: Write a program that finds the largest and smallest number in list.

numbers = [55, 1, 3, 95, 36, 74, 22]

numbers.sort()

print(f"""Smallest number: {numbers[0]}
Largest number: {numbers[-1]}""")