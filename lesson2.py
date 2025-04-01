# Cơ chế dynamic python
# Variable (biến) dynamic python
# Khai báo biến

a = 100
b = 'thanh luong'
print(a)
print(b)

# kiểu dữ liệu
# số nguyên (Interger)
a = 100
print('a =', a)
print('kiểu dữ liệu:', type(a))
# số thực (floating point number)
b = 100.5
print('kiểu dữ liệu:', type(b))
print('b =', b)
# số phức (complex number)
c = 100 + 5j
print('c =', c)
print('kiểu dữ liệu:', type(c))

# kiểu bool (boolean)
d = True
print('d =', type(d))

# kiểu string (string)
e = 'Hello'
print('e =', e)
print('kiểu dữ liệu:', type(e))


# Ép kiểu (casting)
# int() - ép kiểu về số nguyên
a = 100.5
b = int(a)
print('b =', b)

# float() - ép kiểu về số thực
a = 100
b = float(a)
print('b =', b)
# complex() - ép kiểu về số phức
a = 100
b = complex(a)
print('b =', b)
# str() - ép kiểu về string
a = 100
b = str(a)
print('b =', b)

# list - danh sách
a = [1, 2, 3]
print('a =', a)
print('kiểu dữ liệu:', type(a))