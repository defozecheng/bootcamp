# Functions with parameters

# def greet_person(name):
#     print(f"Hello, {name}!")

# greet_person("Alice")
# greet_person("John")


# def lala(name):
#     print(f"I love you, {name}!")


# lala("亲爱的")
# lala(123)

# Function with return values

# def add_number(a,b):
#     return a + b

# result = add_number(5,3)
# print(result)

# Default parameters
# def greet_with_title(name, title="Mr."):
#     return f"Hello, {title} {name}!"

# print(greet_with_title("Smith"))
# print(greet_with_title("Johnson", "Dr."))
# print(greet_with_title(12,996))

# *args - variable number of arguments
# def sum_all(*args):
#     return sum(args)

# print(sum_all(1,2,3,4,5))
# print(sum_all(*range(1,15)))

# **kwargs - keyword arguements
# def print_info(**kwargs):
#     for key, value in kwargs.items():
#         print(f"{key}:{value}")

# print_info(name="Alice",age=25,city="New York")
# print_info(abc="ababab",defg=1.98566,eddfgas="639988")

# Combining *args and **kwargs
# def flexible_function(*args,**kwargs):
#     print("Positional arguements:", args)
#     print("Keyword arguements:",kwargs)

# flexible_function(1, 2, 3, name="Alice, age=25")

# Lambda functions (anonymous functions)
# square = lambda x: x**2
# print(square(5))                        #25

# add = lambda x, y: x + y
# print(add(3, 4))                        #7


# Exercise 1: Write a function that checks if a number is prime.

# def prime(x):
#     if x <= 1:
#         print("Not a Prime")

#     else:
#         is_prime = True

#         for i in range(2,x):
#            if x % i == 0: 
#                is_prime = False
#                print("Not Prime")
#                break

#         if is_prime:
#             print("Prime")


# prime(67)
            
# Exercise 2: Build a temperature converter function. (Celsius to Fahrenheit)

c_to_f = lambda x: x * 9 / 5 + 32
print(f"{c_to_f(100)}°F")
