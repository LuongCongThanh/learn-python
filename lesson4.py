# Trong Python, bạn có thể nhập dữ liệu từ bàn phím bằng cách sử dụng hàm input().
# Hàm input() sẽ dừng chương trình và chờ người dùng nhập dữ liệu từ bàn phím.
# Sau khi người dùng nhập dữ liệu và nhấn Enter, hàm input() sẽ trả về chuỗi dữ liệu mà người dùng đã nhập.
# Dưới đây là một ví dụ đơn giản về cách sử dụng hàm input() trong Python:
# Nhập tên người dùng
name = input("Nhập tên của bạn: ")
# In ra lời chào
print("Xin chào, " + name + "! Chào mừng bạn đến với Python.")
# ví dụ tính chu vi hinh chữ nhật
# Nhập chiều dài và chiều rộng của hình chữ nhật
length = float(input("Nhập chiều dài của hình chữ nhật: "))
width = float(input("Nhập chiều rộng của hình chữ nhật: "))
# Tính chu vi của hình chữ nhật
perimeter = 2 * (length + width)
# In ra chu vi
print("Chu vi của hình chữ nhật là:", perimeter)

# Nhập một số nguyên
number = int(input("Nhập một số nguyên: "))
# Kiểm tra xem số đó là số chẵn hay số lẻ
if number % 2 == 0:
    print(number, "là số chẵn.")
else:
    print(number, "là số lẻ.")

# Nhập một số thực
number = float(input("Nhập một số thực: "))
# Kiểm tra xem số đó là số dương, âm hay bằng 0
if number > 0:
    print(number, "là số dương.")
elif number < 0:
    print(number, "là số âm.")
else:
    print(number, "bằng 0.")

# Nhập nhiều giá trị cùng lúc
values = input("Nhập nhiều giá trị cách nhau bởi dấu phẩy: ")
# Tách các giá trị và chuyển đổi thành danh sách
values_list = values.split(",")
# In ra danh sách các giá trị
print("Danh sách các giá trị:", values_list)
