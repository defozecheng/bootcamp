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
try:
    file = open("data.txt", "r")
except FileNotFoundError:
    print("File not found!")
else:
    content = file.read()
    print("File read successfully")
finally:
    if 'file' in locals() and not file.closed:
        file.close()
    print("Cleanup completed")


