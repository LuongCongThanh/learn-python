# The provided code stub will read in a dictionary containing key/value pairs of name:[marks] for a list of students. Print the average of the marks array for the student name provided, showing 2 places after the decimal.

if __name__ == '__main__':
    n = int(input().strip())
    student_marks = {}

    for _ in range(n):
        data = input().split()
        name = data[0]
        marks = list(map(float, data[1:]))
        student_marks[name] = marks

    query_name = input().strip()

    if query_name in student_marks:
        avg_marks = sum(student_marks[query_name]) / len(student_marks[query_name])
        print(f"{avg_marks:.2f}")