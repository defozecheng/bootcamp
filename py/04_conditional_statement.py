#write a program that categorize BMI (Body Mass Index) into underweight(<18.5),normal weight(<24.9),overweight(<29.9), and obesity(>30), formula = kg/m^2)

while True:
    try:
        Weight = float(input("Enter your weight in KG: "))
        break
    except ValueError:
        print("Enter valid number.")

while True:
    try:
        Height = float(input("Enter your height in M: "))
        break
    except ValueError:
        print("Enter valid number.")

bmi = Weight / Height ** 2
if bmi < 18.5:
    category = "Underweight"
elif bmi<24.9:
    category = "Normal weight"
elif bmi<29.9:
    category = "Overweight"
elif bmi>30.0:
    category = "Obesity"

print(f"Your BMI is: {bmi:.3f}")
print(f"Your Category: {category}")

