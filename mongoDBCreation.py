from faker import Faker
import random
import pandas as pd
from datetime import timedelta, datetime
from sqlalchemy import create_engine
from pymongo import MongoClient

# Initialize Faker
faker = Faker()

# Create a database connection (SQLite example)
engine = create_engine("sqlite:///synthetic_university.db")

# Helper functions
def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

def save_to_db(df, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)

def save_to_csv(df, file_name):
    df.to_csv(file_name, index=False)

def save_to_mongo(df, collection_name):
    db[collection_name].insert_many(df.to_dict(orient="records"))


# Generate Departments
def generate_departments(num_departments=10):
    return pd.DataFrame({
        "department_id": range(1, num_departments + 1),
        "department_name": [f"Department {faker.word().capitalize()}" for _ in range(num_departments)],
        "hod_id": [None] * num_departments  # Temporary, will assign staff later
    })

# Generate Staff
def generate_staff(num_staff=50, num_departments=10):
    staff = pd.DataFrame({
        "staff_id": range(1, num_staff + 1),
        "first_name": [faker.first_name() for _ in range(num_staff)],
        "last_name": [faker.last_name() for _ in range(num_staff)],
        "email": [faker.unique.email() for _ in range(num_staff)],
        "dob": [faker.date_of_birth(minimum_age=25, maximum_age=60) for _ in range(num_staff)],
        "hire_date": [random_date(datetime(2000, 1, 1), datetime(2020, 1, 1)) for _ in range(num_staff)],
        "department_id": [random.randint(1, num_departments) for _ in range(num_staff)]
    })
    return staff

# Generate Students
def generate_students(num_students=1000):
    return pd.DataFrame({
        "student_id": range(1, num_students + 1),
        "first_name": [faker.first_name() for _ in range(num_students)],
        "last_name": [faker.last_name() for _ in range(num_students)],
        "email": [faker.unique.email() for _ in range(num_students)],
        "dob": [faker.date_of_birth(minimum_age=18, maximum_age=25) for _ in range(num_students)],
        "gender": [random.choice(["M", "F"]) for _ in range(num_students)],
        "enrollment_date": [random_date(datetime(2015, 1, 1), datetime(2024, 1, 1)) for _ in range(num_students)]
    })

# Generate Courses
def generate_courses(num_courses=50, num_departments=10):
    return pd.DataFrame({
        "course_id": range(1, num_courses + 1),
        "course_name": [f"{faker.word().capitalize()} 101" for _ in range(num_courses)],
        "course_description": [faker.text() for _ in range(num_courses)],
        "credits": [random.randint(1, 5) for _ in range(num_courses)],
        "department_id": [random.randint(1, num_departments) for _ in range(num_courses)]
    })

# Generate Classrooms
def generate_classrooms(num_classrooms=10):
    return pd.DataFrame({
        "classroom_id": range(1, num_classrooms + 1),
        "room_number": [f"Room {i}" for i in range(1, num_classrooms + 1)],
        "capacity": [random.randint(20, 100) for _ in range(num_classrooms)],
        "building_name": [f"Building {random.randint(1, 5)}" for _ in range(num_classrooms)]
    })

# Generate Schedules
def generate_schedules(num_schedules=100, courses=None, classrooms=None, staff=None):
    return pd.DataFrame({
        "schedule_id": range(1, num_schedules + 1),
        "course_id": [random.choice(courses["course_id"]) for _ in range(num_schedules)],
        "classroom_id": [random.choice(classrooms["classroom_id"]) for _ in range(num_schedules)],
        "staff_id": [random.choice(staff["staff_id"]) for _ in range(num_schedules)],
        "day_of_week": [random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]) for _ in range(num_schedules)],
        "start_time": [faker.time(pattern="%H:%M:%S") for _ in range(num_schedules)],
        "end_time": [faker.time(pattern="%H:%M:%S") for _ in range(num_schedules)]
    })

# Generate Enrollments
def generate_enrollments(num_enrollments=1000, students=None, courses=None):
    return pd.DataFrame({
        "enrollment_id": range(1, num_enrollments + 1),
        "student_id": [random.choice(students["student_id"]) for _ in range(num_enrollments)],
        "course_id": [random.choice(courses["course_id"]) for _ in range(num_enrollments)],
        "enrollment_date": [random_date(datetime(2015, 1, 1), datetime(2024, 1, 1)) for _ in range(num_enrollments)]
    })

# Generate Grades
def generate_grades(num_grades=1000, students=None, courses=None):
    return pd.DataFrame({
        "grade_id": range(1, num_grades + 1),
        "student_id": [random.choice(students["student_id"]) for _ in range(num_grades)],
        "course_id": [random.choice(courses["course_id"]) for _ in range(num_grades)],
        "grade": [random.choice(["A", "B", "C", "D", "F"]) for _ in range(num_grades)],
        "graded_on": [random_date(datetime(2020, 1, 1), datetime(2024, 1, 1)) for _ in range(num_grades)]
    })

# Generate Attendance
def generate_attendance(num_records=1000, students=None, schedules=None):
    return pd.DataFrame({
        "attendance_id": range(1, num_records + 1),
        "student_id": [random.choice(students["student_id"]) for _ in range(num_records)],
        "schedule_id": [random.choice(schedules["schedule_id"]) for _ in range(num_records)],
        "attendance_date": [random_date(datetime(2020, 1, 1), datetime(2024, 1, 1)) for _ in range(num_records)],
        "status": [random.choice(["Present", "Absent"]) for _ in range(num_records)]
    })

# Generate Libraries
def generate_libraries(num_libraries=5):
    return pd.DataFrame({
        "library_id": range(1, num_libraries + 1),
        "library_name": [f"Library {faker.word().capitalize()}" for _ in range(num_libraries)],
        "location": [faker.address() for _ in range(num_libraries)],
        "capacity": [random.randint(50, 500) for _ in range(num_libraries)]
    })

# Generate Books
def generate_books(num_books=200, libraries=None):
    return pd.DataFrame({
        "book_id": range(1, num_books + 1),
        "title": [faker.text(max_nb_chars=50).strip('.') for _ in range(num_books)],
        "author": [faker.name() for _ in range(num_books)],
        "isbn": [faker.unique.isbn13() for _ in range(num_books)],
        "library_id": [random.choice(libraries["library_id"]) for _ in range(num_books)]
    })

# Generate Library Memberships
def generate_library_memberships(num_memberships=500, students=None, libraries=None):
    return pd.DataFrame({
        "membership_id": range(1, num_memberships + 1),
        "student_id": [random.choice(students["student_id"]) for _ in range(num_memberships)],
        "library_id": [random.choice(libraries["library_id"]) for _ in range(num_memberships)],
        "start_date": [random_date(datetime(2015, 1, 1), datetime(2024, 1, 1)) for _ in range(num_memberships)],
        "end_date": [None if random.random() < 0.2 else random_date(datetime(2024, 1, 2), datetime(2025, 1, 1)) for _ in range(num_memberships)]
    })

# Generate Borrowed Books
def generate_borrowed_books(num_borrows=1000, memberships=None, books=None):
    return pd.DataFrame({
        "borrow_id": range(1, num_borrows + 1),
        "membership_id": [random.choice(memberships["membership_id"]) for _ in range(num_borrows)],
        "book_id": [random.choice(books["book_id"]) for _ in range(num_borrows)],
        "borrowed_on": [random_date(datetime(2020, 1, 1), datetime(2024, 1, 1)) for _ in range(num_borrows)],
        "due_date": [random_date(datetime(2024, 1, 2), datetime(2025, 1, 1)) for _ in range(num_borrows)],
        "returned_on": [None if random.random() < 0.3 else random_date(datetime(2024, 1, 2), datetime(2025, 1, 1)) for _ in range(num_borrows)]
    })

# Generate Events
def generate_events(num_events=50, staff=None):
    return pd.DataFrame({
        "event_id": range(1, num_events + 1),
        "event_name": [faker.text(max_nb_chars=50).strip('.') for _ in range(num_events)],
        "event_date": [random_date(datetime(2020, 1, 1), datetime(2024, 12, 31)) for _ in range(num_events)],
        "location": [faker.address() for _ in range(num_events)],
        "organized_by": [random.choice(staff["staff_id"]) for _ in range(num_events)]
    })

# Generate Student Clubs
def generate_student_clubs(num_clubs=20, staff=None):
    return pd.DataFrame({
        "club_id": range(1, num_clubs + 1),
        "club_name": [f"Club {faker.word().capitalize()}" for _ in range(num_clubs)],
        "created_on": [random_date(datetime(2015, 1, 1), datetime(2024, 1, 1)) for _ in range(num_clubs)],
        "advisor_id": [random.choice(staff["staff_id"]) for _ in range(num_clubs)]
    })

# Generate Club Memberships
def generate_club_memberships(num_memberships=500, students=None, clubs=None):
    return pd.DataFrame({
        "membership_id": range(1, num_memberships + 1),
        "student_id": [random.choice(students["student_id"]) for _ in range(num_memberships)],
        "club_id": [random.choice(clubs["club_id"]) for _ in range(num_memberships)],
        "joined_on": [random_date(datetime(2015, 1, 1), datetime(2024, 1, 1)) for _ in range(num_memberships)],
        "role": [random.choice(["President", "Vice President", "Member", "Treasurer", "Secretary"]) for _ in range(num_memberships)]
    })



# Main function
def main():
    # Generate data
    departments = generate_departments()
    staff = generate_staff(num_staff=100, num_departments=len(departments))
    students = generate_students(num_students=1000)
    courses = generate_courses(num_courses=50, num_departments=len(departments))
    classrooms = generate_classrooms(num_classrooms=10)
    schedules = generate_schedules(num_schedules=100, courses=courses, classrooms=classrooms, staff=staff)
    enrollments = generate_enrollments(num_enrollments=1000, students=students, courses=courses)
    grades = generate_grades(num_grades=500, students=students, courses=courses)
    attendance = generate_attendance(num_records=1000, students=students, schedules=schedules)
    libraries = generate_libraries()
    books = generate_books(libraries=libraries)
    memberships = generate_library_memberships(students=students, libraries=libraries)
    borrowed_books = generate_borrowed_books(memberships=memberships, books=books)
    events = generate_events(staff=staff)
    clubs = generate_student_clubs(staff=staff)
    club_memberships = generate_club_memberships(students=students, clubs=clubs)

    # Assign HoDs to departments
    hods = staff.sample(len(departments))
    departments["hod_id"] = hods["staff_id"].values

    # MongoDB connection
    client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
    db = client["university_db"]

    # Save data
    save_to_csv(departments, "Departments.csv")
    save_to_csv(staff, "Staff.csv")
    save_to_csv(students, "Students.csv")
    save_to_csv(courses, "Courses.csv")
    save_to_csv(classrooms, "Classrooms.csv")
    save_to_csv(schedules, "Schedules.csv")
    save_to_csv(enrollments, "Enrollments.csv")
    save_to_csv(grades, "Grades.csv")
    save_to_csv(attendance, "Attendance.csv")
    save_to_csv(libraries, "Libraries.csv")
    save_to_csv(books, "Books.csv")
    save_to_csv(memberships, "LibraryMemberships.csv")
    save_to_csv(borrowed_books, "BorrowedBooks.csv")
    save_to_csv(events, "Events.csv")
    save_to_csv(clubs, "StudentClubs.csv")
    save_to_csv(club_memberships, "ClubMemberships.csv")

    print("Data generation completed!")

if __name__ == "__main__":
    main()
