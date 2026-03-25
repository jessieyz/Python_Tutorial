grade = input("Enter your score:")
if grade.isnumeric():
    grade = int(grade)
    if grade >= 90:
        print("A")
    elif grade >= 80:
        print("B")
    elif grade >= 70:
        print("C")
    elif grade >= 60:
        print("D")
    else:
        print("F")
else:
    print("Invalid input. Please enter a numeric score.")