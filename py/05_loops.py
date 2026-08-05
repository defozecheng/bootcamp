#Exercise 1: Create a multiplication table generator

# number = int(input("Enter a number: "))
# for i in range(1,13):
#     print(f"{i} x {number} = {i*number}")


# Exercise 2: Write a program that finds all prime numbers up to a given number. (limit=20)

# Method 1

for i in range(2,21):
    for j in range(2,i):
        if i % j == 0:
            break
    else:
        print(i)

# Method 2
limit = 20

for num in range(2, limit +1):
    is_prime = True
    for i in range(2, num):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num)






