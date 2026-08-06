# Basic class defination

class Person:
    species = "Homo sapiens"

    def __init__(self, name, age, born):
            self.name = name
            self.age = age
            self.born = born

    def introduction(self):
          return f"Hi, I'm {self.name} and I'm {self.age} years old. I'm born in {self.born}."

    def have_birthday(self):
          self.age += 1
          return f"Happy birthday! {self.name} from {self.born} is now {self.age}."

    
person1 = Person("Alice",25,"Kuala Lumpur")
person2 = Person("Bob",30,"Georgetown")

print(person1.name)
print(person1.born)
print(person2.age)
print(person2.name)

print(person1.introduction())
print(person2.have_birthday())

print(Person.species)
print(person1.species)
