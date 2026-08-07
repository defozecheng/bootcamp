# Basic class defination

# class Person:
#     # Class attribute (shared by all instances)
#     species = "Homo sapiens"

#     # Constructor method
#     def __init__(self, name, age, born):
#             # Instance attributes
#             self.name = name
#             self.age = age
#             self.born = born

#     # Instance method
#     def introduction(self):
#           return f"Hi, I'm {self.name} and I'm {self.age} years old. I'm born in {self.born}."

#     # Method with parameters
#     def have_birthday(self):
#           self.age += 1
#           return f"Happy birthday! {self.name} from {self.born} is now {self.age}."

# # Creating objects (instances)    
# person1 = Person("Alice",25,"Kuala Lumpur")
# person2 = Person("Bob",30,"Georgetown")

# # Acessing attributes
# print(person1.name)         # "Alice"
# print(person1.born)         # "Kuala Lumpur"
# print(person2.age)          # 30
# print(person2.name)         # "Bob"

# # Calling methods
# print(person1.introduction())
# print(person2.have_birthday())

# # Class attributes
# print(Person.species)       # "Homo sapiens"    
# print(person1.species)      # "Homo sapiens"

#----------------------------------------------------------------------

# class BankAccount:
#     def __init__(self, account_number, owner, balance=0):
#         self.account_number = account_number
#         self.owner = owner
#         self.balance = balance
#         self.transaction_history = []

#     def deposit(self,amount):
#         if amount > 0:
#             self.balance += amount
#             self.transaction_history.append(f"Deposited ${amount}")
#             return f"""Deposited ${amount}.
# New Balance: ${self.balance}"""
#         else:
#             return "Invalid deposit amount"

#     def withdraw (self,amount):
#         if amount > 0 and amount <= self.balance:
#             self.balance -= amount
#             self.transaction_history.append(f"Withdrew ${amount}")
#             return f"""Withdrew ${amount}.
# New Balance: ${self.balance}"""
#         else:
#             return "Invalid withdrawal amount or insufficient funds"

#     def get_balance(self):
#         return f"Current balance: ${self.balance}"

#     def get_transaction_history(self):
#         return self.transaction_history

# # Using the BankAccount class
# account = BankAccount("12345", "Alice", 1000)
# print(account.deposit(500))
# print(account.withdraw(200))
# print(account.get_balance())
# print(account.get_transaction_history())


# Ecercise: Create a simple game character class with health, attack andheal methods.

class Character:
    def __init__(self,health = 100, attack = 1, heal):
        