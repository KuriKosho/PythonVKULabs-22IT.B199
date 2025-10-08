# Bài 1
number = int(input("Enter your positive integer: "))
if number % 2 == 0:
    print("Đây là số chẵn")
else:
    print("Đây là số lẻ")

# Bài 2
st = input("Enter your string: ")
if st.isupper():
    print("This is an upper string")
elif st.islower():
    print("This is a lower string")
else:
    print("This string contains upper and lower characters")

# Bài 3
st = input("Enter your string: ")
st_search = input("Enter a searching string: ")
if st_search in st:
    print("Đã tìm thấy chuỗi cần tìm, tại vị trí:", st.find(st_search))
else:
    print("Không tìm thấy")

# Bài 4
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
num3 = float(input("Enter third number: "))

if (num1 >= num2) and (num1 >= num3):
    largest = num1
elif (num2 >= num1) and (num2 >= num3):
    largest = num2
else:
    largest = num3

print("The largest number between", num1, ",", num2, "and", num3, "is", largest)

# Bài 5
n = int(input("Enter an integer greater than 0: "))
total = 0.0
for i in range(1, n + 1):
    total += i / (i + 1)
print(total)

# Bài 6
st = input("Enter your sentence: ")
sum_upper_char = 0
sum_lower_char = 0
for c in st:
    if c.isupper():
        sum_upper_char += 1
    elif c.islower():
        sum_lower_char += 1
print("Chữ hoa:", sum_upper_char)
print("Chữ thường:", sum_lower_char)

# Bài 7
num = int(input("Enter a number: "))
level = int(input("Bậc: "))
total = 0
temp = num
while temp > 0:
    digit = temp % 10
    total += digit ** level
    temp //= 10
if num == total:
    print(num, "is Armstrong, level:", level)
else:
    print(num, "is not Armstrong")

# Bài 8
my_str = input("Enter a string: ")
st2 = ""
for char in my_str:
    if char.isalnum() or char.isspace():
        st2 += char
print(st2)

# Bài 9
my_str = input("Enter a string: ")
ds_tu = my_str.split()
ds_tu.sort()
print("Các từ đã được tách và sắp xếp theo Alphabe")
for tu in ds_tu:
    print(tu)

# Bài 10
total = 0
count = 0
while True:
    inp = input("Enter a number (type 'done' to finish): ")
    if inp == "done":
        break
    try:
        value = float(inp)
        total += value
        count += 1
    except ValueError:
        print("Invalid input, please enter a number.")
if count > 0:
    average = total / count
    print("Average is:", average)
else:
    print("No numbers entered.")

# Bài 11
numlist = []
while True:
    inp = input("Enter a number (type 'done' to finish): ")
    if inp == "done":
        break
    try:
        value = float(inp)
        numlist.append(value)
    except ValueError:
        print("Invalid input, please enter a number.")
if numlist:
    average = sum(numlist) / len(numlist)
    print("Giá trị Trung bình:", average)
    print(numlist)
else:
    print("No numbers entered.")

# Bài 12
result = []
for i in range(2000, 3201):
    if i % 7 == 0 and i % 5 != 0:
        result.append(str(i))
print(",".join(result))

# Bài 13
lines = []
while True:
    s = input()
    if s:
        lines.append(s.upper())
    else:
        break
for sentence in lines:
    print(sentence)

# Bài 14
values = []
for i in range(100, 301):
    s = str(i)
    if all(int(digit) % 2 == 0 for digit in s):
        values.append(s)
print(",".join(values))

# Bài 15
chuoi = input("Nhập vào các giá trị: ")
kieu_ds = chuoi.split(",")
kieu_tuples = tuple(kieu_ds)
print(kieu_ds)
print(kieu_tuples)

# Bài 16
n = int(input("Nhập vào một số: "))
d = {}
for i in range(1, n + 1):
    d[i] = i * i
print(d)

# Bài 17
chuoi = input("Nhập vào một câu: ")
d = {"chu_cai": 0, "chu_so": 0}
for ch in chuoi:
    if ch.isalpha():
        d["chu_cai"] += 1
    elif ch.isdigit():
        d["chu_so"] += 1
print("Số chữ cái là:", d["chu_cai"])
print("Số chữ số là:", d["chu_so"])

# Bài 18
chuoi = input("Nhập vào một câu: ")
d = {"chu_hoa": 0, "chu_thuong": 0}
for ch in chuoi:
    if ch.isupper():
        d["chu_hoa"] += 1
    elif ch.islower():
        d["chu_thuong"] += 1
print("Số chữ hoa là:", d["chu_hoa"])
print("Số chữ thường là:", d["chu_thuong"])

# Bài 19
ftext = open("romeo.txt")
tu_dien_cac_tu = {}
for dong in ftext:
    danh_sach_tu = dong.split()
    for tu in danh_sach_tu:
        tu_dien_cac_tu[tu] = tu_dien_cac_tu.get(tu, 0) + 1

danh_sach = []
for key, val in tu_dien_cac_tu.items():
    newtup = (val, key)
    danh_sach.append(newtup)

danh_sach = sorted(danh_sach, reverse=True)

for val, key in danh_sach[:10]:
    print(key, val)

ftext.close()

# Bài 20
x = int(input("Nhập số cần tính giai thừa: "))
def giaithua(x):
    if x == 0:
        return 1
    return x * giaithua(x - 1)
print("Giai thừa của", x, "là:", giaithua(x))

# Bài 21
def Tao_In_DS():
    ds = []
    for i in range(1, 21):
        ds.append(i ** 2)
    print(ds)

Tao_In_DS()

# Bài 22
def Tao_In_DS_22():
    ds = []
    for i in range(1, 21):
        ds.append(i ** 2)
    print(ds[:5] + ds[-5:])

Tao_In_DS_22()

# Bài 23
def Check_chan(x):
    if x % 2 == 0:
        print(x, "là số chẵn")
    else:
        print(x, "là số lẻ")

x = int(input("Nhập số cần kiểm tra: "))
Check_chan(x)

# Bài 23
# So_Sanh_Chuoi.py
def printValue(s1, s2):
    len1 = len(s1)
    len2 = len(s2)
    if len1 > len2:
        print("Chuỗi dài hơn:", s1)
    elif len2 > len1:
        print("Chuỗi dài hơn:", s2)
    else:
        print(s1)
        print(s2)

s1 = input("Nhập chuỗi thứ nhất: ")
s2 = input("Nhập chuỗi thứ hai: ")
printValue(s1, s2)

# Bài 24
def Tao_TD(Max):
    td = {}
    for i in range(1, Max + 1):
        td[i] = i ** 2
    return td

def Print_Item(TD):
    for key, value in TD.items():
        print(f"{key}: {value}")

def Print_Key(TD):
    for key in TD.keys():
        print(key)

def Print_Value(TD):
    for value in TD.values():
        print(value)


Max = int(input("Nhập số Max: "))
TD = Tao_TD(Max)

print("Các phần tử của từ điển:")
Print_Item(TD)

print("Các key của từ điển:")
Print_Key(TD)

print("Các value của từ điển:")
Print_Value(TD)

# Bài 25
# tu_dien.py
def tao_TD(Max):
    d = dict()
    for i in range(1, Max + 1):
        d[i] = i ** 2
    return d

def Print_Item(TD):
    for k, v in TD.items():
        print(k, v)

def Print_key(TD):
    for k in TD.keys():
        print(k)

def Print_value(TD):
    for v in TD.values():
        print(v)

# Test_TD.py
max = int(input("Nhập chỉ số Max: "))
TD = tao_TD(max)
print("Các phần tử của từ điển là:")
Print_Item(TD)
print("Khóa các ph.tử của từ điển:")
Print_key(TD)
print("Giá trị các ph.tử của từ điển:")
Print_value(TD)

# Bài 26
char = input("Enter a letter: ").lower()
if char in ['a', 'e', 'i', 'o', 'u']:
    print(f"{char} is a vowel.")
elif char == 'y':
    print(f"{char} can be a vowel or a consonant.")
elif char.isalpha() and len(char) == 1:
    print(f"{char} is a consonant.")
else:
    print("Invalid input. Please enter a single letter.")

# Bài 27
sides = int(input("Enter the number of sides (3-10): "))
shapes = {
    3: "Triangle",
    4: "Quadrilateral",
    5: "Pentagon",
    6: "Hexagon",
    7: "Heptagon",
    8: "Octagon",
    9: "Nonagon",
    10: "Decagon"
}
if sides in shapes:
    print(f"A shape with {sides} sides is a {shapes[sides]}.")
else:
    print("Error: Number of sides must be between 3 and 10.")

# Bài 28
month = input("Enter the name of a month: ").strip().lower()
days_in_month = {
    "january": 31,
    "february": "28 or 29",
    "march": 31,
    "april": 30,
    "may": 31,
    "june": 30,
    "july": 31,
    "august": 31,
    "september": 30,
    "october": 31,
    "november": 30,
    "december": 31
}
if month in days_in_month:
    print(f"{month.capitalize()} has {days_in_month[month]} days.")
else:
    print("Invalid month name.")

# Bài 29
a = float(input("Enter length of side a: "))
b = float(input("Enter length of side b: "))
c = float(input("Enter length of side c: "))

if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("Equilateral triangle")
    elif a == b or b == c or a == c:
        print("Isosceles triangle")
    else:
        print("Scalene triangle")
else:
    print("The lengths do not form a triangle")

# Bài 30
a = float(input("Enter length of side a: "))
b = float(input("Enter length of side b: "))
c = float(input("Enter length of side c: "))

if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("Equilateral triangle")
    elif a == b or b == c or a == c:
        print("Isosceles triangle")
    else:
        print("Scalene triangle")
else:
    print("The lengths do not form a triangle")


# Bài 31
def caesar_encrypt(message):
    result = ""
    for char in message:
        if char.isupper():
            result += chr((ord(char) - 65 + 3) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - 97 + 3) % 26 + 97)
        else:
            result += char
    return result

msg = input("Enter your message: ")
print("Encrypted message:", caesar_encrypt(msg))

# Bài 32
def caesar_cipher(message, shift, mode):
    result = ""
    for char in message:
        if char.isupper():
            base = 65
            if mode == "encrypt":
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += chr((ord(char) - base - shift) % 26 + base)
        elif char.islower():
            base = 97
            if mode == "encrypt":
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

msg = input("Enter your message: ")
mode = input("Choose mode (encrypt/decrypt): ").strip().lower()
shift = int(input("Enter shift value: "))
print("Result:", caesar_cipher(msg, shift, mode))

# Bài 33
s = input("Enter a string: ")
is_palindrome = True
for i in range(len(s) // 2):
    if s[i] != s[-(i + 1)]:
        is_palindrome = False
        break
if is_palindrome:
    print(f'"{s}" is a palindrome.')
else:
    print(f'"{s}" is not a palindrome.')

# Bài 34
num = int(input("Enter a decimal number: "))
binary = ""
if num == 0:
    binary = "0"
else:
    n = num
    while n > 0:
        binary = str(n % 2) + binary
        n //= 2
print(f"Binary representation of {num} is: {binary}")

# Bài 35
nums = input("Enter numbers separated by commas: ")
num_list = [int(x) for x in nums.split(",")]
odd_list = [x for x in num_list if x % 2 != 0]
print("Odd numbers:", odd_list)

# Bài 36
numbers = []
while True:
    n = int(input("Enter an integer (0 to stop): "))
    if n == 0:
        break
    numbers.append(n)
numbers.sort()
print("Sorted numbers:")
for num in numbers:
    print(num)

# Bài 37
words = []
seen = set()
while True:
    word = input("Enter a word (blank to finish): ")
    if word == "":
        break
    if word not in seen:
        words.append(word)
        seen.add(word)
for w in words:
    print(w)

# Bài 38
negatives = []
zeros = []
positives = []

while True:
    inp = input("Enter an integer (blank to finish): ")
    if inp == "":
        break
    try:
        num = int(inp)
        if num < 0:
            negatives.append(num)
        elif num == 0:
            zeros.append(num)
        else:
            positives.append(num)
    except ValueError:
        print("Invalid input, please enter an integer.")

result = negatives + zeros + positives
for n in result:
    print(n)

# Bài 39
n = int(input("Enter an integer n: "))
d = {}
for i in range(1, n + 1):
    d[i] = i * i
print(d)

# Bài 40
t = (1,2,3,4,5,6,7,8,9,10)
half = len(t) // 2
print(t[:half])
print(t[half:])

# Bài 41
t = (1,2,3,4,5,6,7,8,9,10)
even_tuple = tuple(x for x in t if x % 2 == 0)
print(even_tuple)

# Bài 42
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

num = int(input("Enter a number: "))
print(str(factorial(num)))

# Bài 43
def print_longer_string(s1, s2):
    if len(s1) > len(s2):
        print(s1)
    elif len(s2) > len(s1):
        print(s2)
    else:
        print(s1)
        print(s2)

str1 = input("Enter first string: ")
str2 = input("Enter second string: ")
print_longer_string(str1, str2)

# Bài 44
def print_squares():
    squares = []
    for i in range(1, 21):
        squares.append(i ** 2)
    print(squares)

print_squares()

# Bài 45
def print_first_five_squares():
    squares = []
    for i in range(1, 21):
        squares.append(i ** 2)
    print(squares[:5])

print_first_five_squares()

# Bài 46
def print_last_five_squares():
    squares = [i ** 2 for i in range(1, 21)]
    print(squares[-5:])

print_last_five_squares()

# Bài 47
def print_squares_except_first_five():
    squares = [i ** 2 for i in range(1, 21)]
    print(squares[5:])

print_squares_except_first_five()

# Bài 48
def average(a, b, c):
    return (a + b + c) / 3

x = float(input("Enter first value: "))
y = float(input("Enter second value: "))
z = float(input("Enter third value: "))
print("Average value:", average(x, y, z))

# Bài 49
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

num = int(input("Enter an integer: "))
if is_prime(num):
    print(f"{num} is a prime number.")
else:
    print(f"{num} is not a prime number.")


# Bài 50
import random

def generate_password():
    length = random.randint(7, 10)
    password = ''.join(chr(random.randint(33, 126)) for _ in range(length))
    return password

print("Random password:", generate_password())

# Bài 51
def is_good_password(password):
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit

pwd = input("Enter your password: ")
if is_good_password(pwd):
    print("Good password.")
else:
    print("Bad password.")

# Bài 52
def is_perfect(n):
    if n < 2:
        return False
    total = sum(i for i in range(1, n) if n % i == 0)
    return total == n

print("Perfect numbers from 1 to 10000:")
for i in range(1, 10001):
    if is_perfect(i):
        print(i)


# Bài 53
def all_sublists(lst):
    result = []
    n = len(lst)
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            result.append(lst[i:j])
    return result

print(all_sublists([1, 2, 3]))

# Bài 54
def format_english_list(words):
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    return ", ".join(words[:-1]) + " and " + words[-1]

# Main program
word_list = []
while True:
    word = input("Enter a word (blank to finish): ").strip()
    if word == "":
        break
    word_list.append(word)
result = format_english_list(word_list)
print("Formatted list:", result)

# Bài 55
import zipfile

def compress_file(input_file, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        zipf.write(input_file)

def decompress_file(zip_file, extract_to='.'):
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        zipf.extractall(extract_to)

# Compress
input_file = input("Enter file to compress: ")
output_zip = input("Enter output zip file name: ")
compress_file(input_file, output_zip)
print("File compressed.")

# Decompress
zip_file = input("Enter zip file to decompress: ")
extract_to = input("Enter folder to extract to (default: current): ") or '.'
decompress_file(zip_file, extract_to)
print("File decompressed.")