# Dictionaries

# student = {
#     "name" : "Alice",
#     "age" : 20,
#     "grade" : "A",
#     "courses" : ["Math","Science","English"]
# }

#Acessing and modifying
# print(student["name"])                      # "Alice"
# print(student.get("age"))                   # 20

# student["age"] = 21                         # Modify value
# student["email"] = "alice@gmail.com"        # Add new key-value

# print(student["age"])                       # 21
# print(student["email"])                     # "alice@gmail.com"

# Dictionaries Method

# keys = student.keys()                         # Get all keys
# values = student.values()                    # Get all values
# items = student.items()                     # Get key-value pairs

# print(keys)
# print(values)
# print(items)

# Iterating Dictionaries

# Iterating through dictionaries
# for key in student:
#     print(f"{key}:{student[key]}")

# for key,value in student.items():
#     print(f"{key}:{value}")


# Nested dictionaries

# company = {
#     "employees" : {
#         "john" : {"age": 30,"department":"IT"},
#         "jane" : {"age": 25,"department":"HR"}
#     },
#     "departments" : ["IT","HR","Finance"]
# }

# print(company["employees"].items())
# print(company["departments"])

# Exercise 1: Create a dictionary called student_records with the following information:"student_001": name is "John", age is 19, major is "Computer Science", grades are [85, 92, 78]"student_002": name is "Sarah", age is 20, major is "Biology", grades are [90, 88, 95]

student_records = {
    "student": {
        "student_001":{"name": "John","age":19, "major": "Computer Science", "grades" : [85, 92, 78]},
        "student_002":{"name":"Sarah","age":20, "major": "Biology", "grades": [90, 88, 95]}
    }
}

# print(student_records["student"].items())

# Exercise 2: Add a new student "student_003" with name "Mike", age 18, major "Math", grades [82, 79, 91]

student_records["student"]["student_003"] = {"name": "Mike", "age": 18, "major": "Math","grades":[82,79,91]}
# print(student_records["student"].items())

# Exercise 3: Update John's age to 20

student_records["student"]["student_001"]["age"] = 20
# print(student_records["student"]["student_001"]["age"])

# Exercise 4: Loop through the dictionary and print each student's information in this format:"Student ID: [id], Name: [name], Major: [major]

for student_id in student_records["student"]:
    print(f"Student ID: {student_id}, Name: {student_records['student'][student_id]['name']}, Major: {student_records['student'][student_id]['major']}")