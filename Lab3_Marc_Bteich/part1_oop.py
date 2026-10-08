"""Part 1: OOP Implementation - School Management System.

Defines Person, Student, Instructor and Course classes with data
validation (email format, non-negative age) and JSON serialization.
"""

import json
import re


# --------------------------------------------------------------------------
# Validation helpers
# --------------------------------------------------------------------------

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")


def validate_email(email):
    """Return the email if it has a valid format, otherwise raise ValueError."""
    if not isinstance(email, str) or not EMAIL_PATTERN.match(email):
        raise ValueError("Invalid email format: " + str(email))
    return email


def validate_age(age):
    """Return the age as an int if it is a non-negative number."""
    try:
        age = int(age)
    except (TypeError, ValueError):
        raise ValueError("Age must be a number, got " + str(age))
    if age < 0:
        raise ValueError("Age must be non-negative, got " + str(age))
    return age


def validate_non_empty(value, field_name):
    """Return the stripped value if it is a non-empty string."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(field_name + " must be a non-empty string")
    return value.strip()


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

class Person:
    """Base class holding the data shared by students and instructors."""

    def __init__(self, name, age, email):
        self.name = validate_non_empty(name, "Name")
        self.age = validate_age(age)
        self._email = validate_email(email)

    def introduce(self):
        """Print a short introduction of the person."""
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = validate_email(email)

    def to_dict(self):
        return {"name": self.name, "age": self.age, "email": self._email}


class Student(Person):
    """A student, identified by a student_id, who registers for courses."""

    def __init__(self, name, age, email, student_id, registered_courses=None):
        super().__init__(name, age, email)
        self.student_id = validate_non_empty(student_id, "Student ID")
        self.registered_courses = list(registered_courses or [])

    def register_course(self, course):
        """Register this student in a course (both sides are linked)."""
        if course not in self.registered_courses:
            self.registered_courses.append(course)
        if self not in course.enrolled_students:
            course.enrolled_students.append(self)

    def introduce(self):
        print(f"Hello, my name is {self.name}, I am {self.age} years old "
              f"and my student ID is {self.student_id}.")

    def to_dict(self):
        data = super().to_dict()
        data["student_id"] = self.student_id
        data["registered_courses"] = [c.course_id for c in self.registered_courses]
        return data


class Instructor(Person):
    """An instructor, identified by an instructor_id, assigned to courses."""

    def __init__(self, name, age, email, instructor_id, assigned_courses=None):
        super().__init__(name, age, email)
        self.instructor_id = validate_non_empty(instructor_id, "Instructor ID")
        self.assigned_courses = list(assigned_courses or [])

    def assign_course(self, course):
        """Assign this instructor to a course (both sides are linked)."""
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
        course.instructor = self

    def introduce(self):
        print(f"Hello, my name is {self.name}, I am {self.age} years old "
              f"and I teach as instructor {self.instructor_id}.")

    def to_dict(self):
        data = super().to_dict()
        data["instructor_id"] = self.instructor_id
        data["assigned_courses"] = [c.course_id for c in self.assigned_courses]
        return data


class Course:
    """A course, taught by one instructor, with a list of enrolled students."""

    def __init__(self, course_id, course_name, instructor=None,
                 enrolled_students=None):
        self.course_id = validate_non_empty(course_id, "Course ID")
        self.course_name = validate_non_empty(course_name, "Course name")
        self.instructor = instructor
        self.enrolled_students = list(enrolled_students or [])

    def add_student(self, student):
        """Enroll a student in this course (both sides are linked)."""
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
        if self not in student.registered_courses:
            student.registered_courses.append(self)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": self.instructor.instructor_id if self.instructor else None,
            "enrolled_students": [s.student_id for s in self.enrolled_students],
        }


# --------------------------------------------------------------------------
# Data management: serialization
# --------------------------------------------------------------------------

def save_data(filename, students, instructors, courses):
    """Save all records to a JSON file."""
    data = {
        "students": [s.to_dict() for s in students],
        "instructors": [i.to_dict() for i in instructors],
        "courses": [c.to_dict() for c in courses],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_data(filename):
    """Load records from a JSON file and rebuild the object relationships.

    Returns a tuple (students, instructors, courses).
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    students = {}
    for d in data.get("students", []):
        students[d["student_id"]] = Student(d["name"], d["age"], d["email"],
                                            d["student_id"])

    instructors = {}
    for d in data.get("instructors", []):
        instructors[d["instructor_id"]] = Instructor(d["name"], d["age"],
                                                     d["email"],
                                                     d["instructor_id"])

    courses = {}
    for d in data.get("courses", []):
        courses[d["course_id"]] = Course(d["course_id"], d["course_name"])

    # Rebuild the links between the objects.
    for d in data.get("courses", []):
        course = courses[d["course_id"]]
        instructor_id = d.get("instructor_id")
        if instructor_id and instructor_id in instructors:
            instructors[instructor_id].assign_course(course)
        for student_id in d.get("enrolled_students", []):
            if student_id in students:
                course.add_student(students[student_id])

    return list(students.values()), list(instructors.values()), list(courses.values())


# --------------------------------------------------------------------------
# Demonstration
# --------------------------------------------------------------------------

if __name__ == "__main__":
    student = Student("Sample Student", 21, "student1@example.com", "S001")
    instructor = Instructor("Sample Instructor", 45, "instructor@example.com", "I001")
    course = Course("EECE435L", "Software Tools Lab")

    instructor.assign_course(course)
    student.register_course(course)

    student.introduce()
    instructor.introduce()
    print(f"{course.course_name} is taught by {course.instructor.name} "
          f"and has {len(course.enrolled_students)} student(s).")

    save_data("435Ldb.json", [student], [instructor], [course])
    students, instructors, courses = load_data("435Ldb.json")
    print(f"Loaded {len(students)} student(s), {len(instructors)} instructor(s), "
          f"{len(courses)} course(s) from 435Ldb.json")

    # Validation examples
    try:
        Student("Bob", -5, "bob@mail.com", "S002")
    except ValueError as error:
        print("Validation error:", error)

    try:
        Student("Bob", 22, "not-an-email", "S003")
    except ValueError as error:
        print("Validation error:", error)
