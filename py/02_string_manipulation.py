# String Creation

# single_quote = 'Hello'
# double_quote = "World"
# triple_quote = """Multi-line
# string"""

# print(single_quote)
# print(double_quote)
# print(triple_quote)



# String indexing and slicing

# text = "Python Programming"

# print(text[0])          # (first character)
# print(text[-1])         # (last character)
# print(text[0:6])        # (slice 0 to 5)
# print(text[:6])         # (from start to 5)
# print(text[7:])         # (7 to end)



# String Methods
# name = " bob the builder "
# print(len(name))                    # Lenght
# print(name.strip())                 # Remove whitespace
# print(name.upper())                 # Uppercase
# print(name.lower())                 # Lowercase
# print(name.title())                 # Title case
# print(name.replace("bob","jane"))   # Replace


# String Formatting

# name = "John Doe"
# age = 30

# message_1 = f"My name is {name} and I am {age} years old."           # f-strings
# message_2 = "My name is {} and I am {} years old.".format(name,age)  # str.format()
# message_3 = "My name is %s and I am %d years old." %(name,age)       # %-formatting

# print(message_1)
# print(message_2)
# print(message_3)



# Exercise: Build  a  simple  text  analyzer  that  counts  words,  characters,  andsentences in a given text.

text = """Python is a powerful programming language. It's easy to learn
and versatile!
You  can  use  Python  for  web  development,  data  science,  
andautomation. The syntax is clean and readable.
This makes Python perfect for beginners and experts alike."""

print(f"Total words = {len(text.split())}")
print(f"Total characters = {len(text)}")
print(text)
