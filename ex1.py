# Viết chương trình nhập vào một danh sách các số nguyên dương và tìm số lớn thứ hai trong danh sách đó.

# arr = list(map(int, input().split(',')))
# # sắp xếp danh sách arr theo thứ tự giảm dần.
# sorted_numbers = sorted(arr, reverse=True)
# second_largest = sorted_numbers[1]
# print(second_largest)

arr = list(map(int, input().split(',')))
unique_numbers = list(set(arr))
if len(unique_numbers) < 2:
    print("Không có số lớn thứ hai")
else:
    unique_numbers.sort(reverse=True)
    print(unique_numbers[1])
