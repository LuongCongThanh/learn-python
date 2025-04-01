# Given the names and grades for each student in a class of N students, store them in a nested list and print the name(s) of any student(s) having the second lowest grade.

# Note: If there are multiple students with the second lowest grade, order their names alphabetically and print each name on a new line.

if __name__ == '__main__':
    N = int(input().strip())

    students = []
    for _ in range(N):
        name = input().strip()
        score = float(input().strip())
        students.append([name, score])

    unique_scores = sorted(set(score for _, score in students))

    if len(unique_scores) < 2:
        exit()

    second_lowest_score = unique_scores[1]

    second_lowest_students = sorted(name for name, score in students if score == second_lowest_score)

    for student in second_lowest_students:
        print(student)


