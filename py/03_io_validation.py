#Input/Output Validation

# name = input("Enter your name: ")
# height = float(input("Enter your height in cm: ")) #Convert to float

# # Input validation
# while True:
#     try:
#         age = int(input("Enter your age: "))
#         if 0 < age < 120:
#             break
#         else:
#             print("Age must be between 1 to 119.")
#     except ValueError:
#         print("Please enter a valid number.")

# # Output validation
# print(f"Hello, {name}!")
# print(f"Your are {age} years old and {height} cm tall.")


#Exercise 1
# Create a simple calculator that takes two number and an operation from user

while True:
    try:
        Number_1 = int(input("Enter your first number:  "))
        break
    except ValueError:
        print("Invalid number, please try again.")

while True:
    try:
        Number_2 = int(input("Enter your second number:  "))
        break
    except ValueError:
        print("Invalid number, please try again.")
Operator = input("Enter an operator (+,-,*,/): ")

while Operator not in ["+","-","*","/"]:
    print ("Invalid Opetator, please try again.")
    Operator = input("Enter an operator (+,-,*,/): ")

if Operator == "+":
    print (f"{Number_1}{Operator}{Number_2}={Number_1 + Number_2}")
elif Operator == "-":
    print (f"{Number_1}{Operator}{Number_2}={Number_1 - Number_2}")
elif Operator == "*":
    print (f"{Number_1}{Operator}{Number_2}={Number_1 * Number_2}")
elif Operator == "/":
    print (f"{Number_1}{Operator}{Number_2}={Number_1 / Number_2}")

#Create a simple quiz progream with 3 questions. At the end of teh quiz, display score/

