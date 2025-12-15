import sqlite3
conn = sqlite3.connect("project.db")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        student_class INTEGER,
        marks INTEGER,
        grade TEXT
    )
    """)

conn.commit()

def register_teacher():
    username = input("Enter teacher username: ")
    password = input("Enter password: ")

    try:
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, 'teacher')",
            (username, password)
        )
        conn.commit()
        print("Teacher registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")


def register_student():
    username = input("Enter student username: ")
    password = input("Enter password: ")
    student_class = int(input("Enter class: "))
    marks = int(input("Enter marks: "))
    grade = input("Enter grade: ")

    try:
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, 'student')",
            (username, password)
        )

        c.execute(
            "INSERT INTO students (username, student_class, marks, grade) VALUES (?, ?, ?, ?)",
            (username, student_class, marks, grade)
        )

        conn.commit()
        print("Student registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")


def login(role):
    username = input("Username: ")
    password = input("Password: ")

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=? AND role=?",
        (username, password, role)
    )

    user = c.fetchone()

    if user:
        print("Login successful!")
        return username
    else:
        print("Invalid login!")
        return None


def add_student():
    username = input("Student username: ")
    student_class = input("Class: ")
    marks = int(input("Marks: "))
    grade = input("Grade: ")

    try:
        c.execute(
            "INSERT INTO students (username, student_class, marks, grade) VALUES (?, ?, ?, ?)",
            (username, student_class, marks, grade)
        )
        conn.commit()
        print("Student added successfully!")
    except sqlite3.IntegrityError:
        print("Student already exists!")


def view_all_students():
    c.execute("SELECT username, student_class, marks, grade FROM students")
    students = c.fetchall()

    print("\n--- Student List ---")
    for s in students:
        print(s)


def update_student():
    username = input("Enter student username: ")
    marks = int(input("New marks: "))
    grade = input("New grade: ")

    c.execute(
        "UPDATE students SET marks=?, grade=? WHERE username=?",
        (marks, grade, username)
    )

    conn.commit()
    print("Student updated successfully!")



def delete_student():
    username = input("Enter student username: ")

    c.execute("DELETE FROM students WHERE username=?", (username,))
    c.execute("DELETE FROM users WHERE username=?", (username,))

    conn.commit()
    print("Student deleted successfully!")


def search_student():
    username = input("Enter student username: ")
    c.execute(
        "SELECT username, student_class, marks, grade FROM students WHERE username=?",
        (username,)
    )

    student = c.fetchone()
    if student:
        print(student)
    else:
        print("Student not found!")


def student_view(username):
    c.execute(
        "SELECT username, student_class, marks, grade FROM students WHERE username=?",
        (username,)
    )

    student = c.fetchone()
    if student:
        print("\n--- Your Details ---")
        print("Username:", student[0])
        print("Class:", student[1])
        print("Marks:", student[2])
        print("Grade:", student[3])
    else:
        print("No record found!")


def main():

    while True:
        print("\n\n            ------ WELCOME BACK ------")
        print("""
        ...... STUDENT GRADING SYSTEM ......
        1. Register Teacher
        2. Register Student
        3. Teacher Login
        4. Student Login
        5. Exit
        """)

        choice = input("Enter choice: ")

        if choice == "1":
            register_teacher()

        elif choice == "2":
            register_student()

        elif choice == "3":
            user = login("teacher")
            if user:
                while True:
                    print("""
                    --- Teacher Menu ---
                    1. Add Student
                    2. View All Students
                    3. Update Student
                    4. Delete Student
                    5. Search Student
                    6. Logout
                    """)
                    ch = input("Enter choice: ")

                    if ch == "1":
                        add_student()
                    elif ch == "2":
                        view_all_students()
                    elif ch == "3":
                        update_student()
                    elif ch == "4":
                        delete_student()
                    elif ch == "5":
                        search_student()
                    elif ch == "6":
                        break

        elif choice == "4":
            user = login("student")
            if user:
                student_view(user)

        elif choice == "5":
            print("Thank you!!...")
            conn.close()
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()

