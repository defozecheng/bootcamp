# Basic exception handling

# try:
#     number = int(input("Enter a number: "))
#     result = 10 / number
#     print(f"Resilt: {result}")
# except ValueError:
#     print("Invalid input! Pleaase enter a number.")
# except ZeroDivisionError:
#     print("Cannot devide by zero!")


# Using else and finally
# try:
#     file = open("data.txt", "r")
# except FileNotFoundError:
#     print("File not found!")
# else:
#     content = file.read()
#     print("File read successfully")
# finally:
#     if 'file' in locals() and not file.closed:
#         file.close()
#     print("Cleanup completed")

# Raising exceptions
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True

try:
    validate_age(155)
except ValueError as e:
    print(f"Validation error: {e}")
