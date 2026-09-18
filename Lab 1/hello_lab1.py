print("==========================")
print("Welcome Here")
print("My First Post!")
print("==========================")

username = "Big_Bob"
bio = "Capturing The Pretty Sights Of The World"
followers = 100

print("Username:", username)
print("Bio:", bio)
print("Followers:", followers)

followers = 100
followers += 50
print("Day 1: ", followers)

followers += 20
print("Day 2: ", followers)

followers -= 10
print("Day 3: ", followers)

username = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("====================")
print("Username:", username)
print("Age:", age)
print("Content Category:", category)

if age>40 and category == "fun":
    print("You are old, what is fun for you?")