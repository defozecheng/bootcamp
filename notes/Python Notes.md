**Chapter 1**



data type

\- string	-> text 		文字

\- integer	-> number		数字

\- float		-> decimal number	小数

\- Boolean	-> True/False		真/假

\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~



example:

name = "Bob"				要加 ” “ 在前后

age = 10

weight = 20.5

is\_female = False			True or False 第一个字母要大写



print(name)				要什么output

print(type(name))			什么类型的data



**Terminal 将会显示-->**

Bob					

<class 'str'>				



class的简写

str = String

int = Integer

float = Float

bool = Boolean



\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~

symbol

\+		Addition		加

\-		Subtraction		减

\*		Multiplication		乘

/		Division		除

//		Floor division		只拿整数去除小数点

%		Modulus			余数

\*\*		Exponentiation		次方 ^2		



\----------------------------------------------------------------------------------------------------------

**Chapter 2**



**String Creation**

single\_quote = 'Hello'			one liner 一行字可以用

double\_quote = "World"			one liner 一行字可以用

triple\_quote = """Multi-line		multi liner 可以显示多行string，根据自己编排

string"""



\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~



**String index and slicing**

Example:



text = "Python Programming"



print(text\[0])          # (first character)		第一个字母

print(text\[-1])         # (last character)		最后一个字母

print(text\[0:6])        # (slice 0 to 5)		第一个到第6个

print(text\[:6])         # (from start to 5)		第一个到第6个

print(text\[7:])         # (7 to end)			7到最后



**Terminal 将会显示-->**

P

g

Python

Python

Programming



all number start from 0，0 is the first number



\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~



**String Methods**

Example:



name = " bob the builder "

print(len(name)）						# Lenght						长度

print(name.strip())						# Remove whitespace			去掉前后空格

print(name.upper())					# Uppercase					全部大写

print(name.lower())					# Lowercase					全部小写

print(name.title())						# Title case					每一个单词开头大写

print(name.replace("bob","jane"))		# Replace					替换

print(name.split())		    # Split			把文字按照空格拆开

print(len(name.split()))	    # Count words		算文字



**Terminal 将会显示-->**

17

bob the builder

&#x20;BOB THE BUILDER 

&#x20;bob the builder 

&#x20;Bob The Builder 

&#x20;jane the builder 

\['bob', 'the', 'builder']



\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~



**String Formatting: 写法**

* f-string
* str.format()
* %-formatting



message\_1 = f"My name is {name} and I am {age} years old."         		  # f-strings

message\_2 = "My name is {} and I am {} years old.".format(name,age)		  # str.format()

message\_3 = "My name is %s and I am %d years old." %(name,age）		  # %-formatting



\----------------------------------------------------------------------------------------------------------







ctrl + / - select and add/remove all#



git add .

git commit -m "your comment"

git push

