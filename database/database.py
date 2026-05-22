import sqlite3

def create_database():
    conn = sqlite3.connect('hms_database.db')
    cursor = conn.cursor()
    #Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        uid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        gpa REAL DEFAULT 0.0,
        rls INTEGER DEFAULT 0,
        credits INTEGER DEFAULT 0,
        attendance_rate REAL DEFAULT 1.0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        course_id TEXT PRIMARY KEY,
        course_name TEXT NOT NULL,
        credits INTEGER NOT NULL,
        prerequisite_id TEXT,
        alternative_course_id TEXT,
        FOREIGN KEY (prerequisite_id) REFERENCES Courses(course_id),
        FOREIGN KEY (alternative_course_id) REFERENCES Courses(course_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CourseClasses (
        class_id TEXT PRIMARY KEY,
        course_id TEXT NOT NULL,
        lecturer_id TEXT NOT NULL,
        attendance_code TEXT,
        FOREIGN KEY (course_id) REFERENCES Courses(course_id),
        FOREIGN KEY (lecturer_id) REFERENCES Users(user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Enrollments (
        class_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        chuyen_can REAL DEFAULT 0.0,
        giua_ky REAL DEFAULT 0.0,
        cuoi_ky REAL DEFAULT 0.0,
        PRIMARY KEY (class_id, student_id),
        FOREIGN KEY (class_id) REFERENCES CourseClasses(class_id),
        FOREIGN KEY (student_id) REFERENCES Users(user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Projects (
        project_id TEXT PRIMARY KEY,
        project_name TEXT NOT NULL,
        student_id TEXT NOT NULL,
        lecturer_id TEXT NOT NULL,
        status TEXT DEFAULT 'Đang thực hiện',
        FOREIGN KEY (student_id) REFERENCES Users(user_id),
        FOREIGN KEY (lecturer_id) REFERENCES Users(user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CompletedCourses (
        student_id TEXT NOT NULL,
        course_id TEXT NOT NULL,
        grade_letter TEXT NOT NULL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES Users(user_id),
        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Khởi tạo CSDL: hms_database.db")

if __name__ == "__main__":
    create_database()