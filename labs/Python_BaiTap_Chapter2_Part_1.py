import math

# Bai 1: Viết chương trình nhập vào một chuỗi ký tự và in ra các biến thể của chuỗi đó:
st = input("Enter your string: ")
st_upper = st.upper()
st_lower = st.lower()
st_title = st.title()

print("A Upper String is: " + st_upper)
print("A Lower String is : " + st_lower)
print("A Title String is : " + st_title)

# Bài 2
data = "minhnhutvh@gmail.com"
position = data.find("@")
host = data[position + 1:]
print(host)  # Output: gmail.com

# Bài 3
data = "minhnhutvh@gmail.com•Sat•Jan•5•09:14:16"
start_position = data.find("@")
end_position = data.find("•", start_position)
host = data[start_position + 1:end_position]
print(host)  # Output: gmail.com

# Bài 4
st1 = input("Enter your string: ")
st2 = input("Enter the word that needs to replace: ")
st3 = input("Enter the word after being replaced: ")

st1 = st1.replace(st2, st3)
print(st1)

# Bài 5
st = input("Enter your string: ")
first_five_characters = st[:5]
last_five_characters = st[-5:]
four_str_one_line = (st + " ") * 4
four_str_four_line = (st + "\n") * 4

print("First five characters are: " + first_five_characters)
print("Last five characters are: " + last_five_characters)
print("Four strings of one line are: " + four_str_one_line.strip())
print("Four strings of four line are:\n" + four_str_four_line.strip())

# Bài 6
r = float(input("Enter the radius (r): "))
h = float(input("Enter the height (h): "))

V = math.pi * r ** 2 * h
print("The volume of the cylinder is:", V)

# Bài 7
a = float(input("Enter side a: "))
b = float(input("Enter side b: "))
c = float(input("Enter side c: "))
A = float(input("Enter angle A (radian): "))
B = float(input("Enter angle B (radian): "))
C = float(input("Enter angle C (radian): "))

# Calculate area using sides a, b and angle C
area = 0.5 * a * b * math.sin(C)
print("The area of the triangle is:", area)

# Bài 8
side = float(input("Enter the side length of the equilateral triangle: "))
s = (3 * side) / 2  # semi-perimeter
area = math.sqrt(s * (s - side) ** 3)
print("The area of the equilateral triangle is:", area)

# Bài 9
# Conclusion:
# Both Bài 7 and Bài 8 will give the same result for the area of an equilateral triangle if you use the same side length and correct angle values. This confirms the correctness of both formulas for this special case.
# However, Bài 7 is more general and can be used for any triangle, while Bài 8 is specific to equilateral triangles only.

# Bài 10
width = float(input("Enter the width of the room: "))
length = float(input("Enter the length of the room: "))

area = width * length
print("The area of the room is:", area)

# Bài 11
length = float(input("Enter the length of the field (meters): "))
width = float(input("Enter the width of the field (meters): "))

area_sqm = length * width
area_acres = area_sqm / 43560

print("The area of the field is:", area_acres, "acres")

# Bài 12
meal_cost = float(input("Enter the cost of the meal: "))

tax = meal_cost * 0.05
tip = meal_cost * 0.18
total = meal_cost + tax + tip

print(f"Meal cost: {meal_cost:.2f}")
print(f"Tax (5%): {tax:.2f}")
print(f"Tip (18%): {tip:.2f}")
print(f"Total amount: {total:.2f}")

# Bài 13
n = int(input("Enter a positive integer n: "))
total = n * (n + 1) // 2
print("The sum of all integers from 1 to", n, "is:", total)

# Bài 14
a = int(input("Enter integer a: "))
b = int(input("Enter integer b: "))

sum_ab = a + b
difference_ab = a - b
product_ab = a * b
quotient_ab = a / b if b != 0 else "undefined (division by zero)"
remainder_ab = a % b if b != 0 else "undefined (division by zero)"
log_a = math.log10(a) if a > 0 else "undefined (log of non-positive number)"
power_ab = a ** b

print(f"Sum of a and b: {sum_ab}")
print(f"Difference of a and b: {difference_ab}")
print(f"Product of a and b: {product_ab}")
print(f"Quotient of a divided by b: {quotient_ab}")
print(f"Remainder when a is divided by b: {remainder_ab}")
print(f"log10(a): {log_a}")
print(f"a raised to the power of b: {power_ab}")

# Bài 15
C = 4.186
JOULE_TO_KWH = 2.777e-7
COST_PER_KWH = 8.9

mass = float(input("Enter mass of water (grams): "))
delta_T = float(input("Enter temperature change (°C): "))

Q = mass * C * delta_T
Q_kWh = Q * JOULE_TO_KWH

cost = Q_kWh * COST_PER_KWH

print(f"\nEnergy required: {Q:.2f} Joules")
print(f"Energy in kWh: {Q_kWh:.6f} kWh")
print(f"Heating cost: {cost:.4f} cents")

# Bài 16
g = 9.8
v_i = 0

d = float(input("Enter the height (meters): "))
v_f = math.sqrt(v_i**2 + 2 * g * d)

print(f"The final velocity when hitting the ground is: {v_f:.2f} m/s")

# Bài 17
Ta = float(input("Enter the air temperature (°C): "))
V = float(input("Enter the wind speed (km/h): "))

WCI = 13.12 + 0.6215 * Ta - 11.37 * V**0.16 + 0.3965 * Ta * V**0.16
WCI_rounded = round(WCI)

print("The wind chill index is:", WCI_rounded)

