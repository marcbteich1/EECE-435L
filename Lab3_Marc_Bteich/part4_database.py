"""Part 4: Database Integration - School Management System.

Defines the SQLite schema for students, instructors, courses and
enrollments, implements the CRUD operations, connects a PyQt5 interface
to the database and provides database backup/restore.

Run "python part4_database.py" to open the database-backed interface,
or "python part4_database.py --demo" to run the CRUD demonstration.
"""

import os
import shutil
import sqlite3
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QComboBox, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QGroupBox, QMessageBox, QFileDialog,
                             QDialog, QFormLayout, QHeaderView)

from part1_oop import validate_email, validate_age, validate_non_empty

DB_NAME = "435Ldb.db"


# --------------------------------------------------------------------------
# Connection and schema
# --------------------------------------------------------------------------

def connect(db_name=DB_NAME):
    """Open a connection to the database with foreign keys enabled."""
    connection = sqlite3.connect(db_name)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables(db_name=DB_NAME):
    """Create the database schema if it does not exist yet."""
    connection = connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name       TEXT NOT NULL,
            age        INTEGER NOT NULL CHECK (age >= 0),
            email      TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            age           INTEGER NOT NULL CHECK (age >= 0),
            email         TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id     TEXT PRIMARY KEY,
            course_name   TEXT NOT NULL,
            instructor_id TEXT,
            FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
                ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id TEXT NOT NULL,
            course_id  TEXT NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students (student_id)
                ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------------------------------------------------
# CRUD: students
# --------------------------------------------------------------------------

def add_student(student_id, name, age, email, db_name=DB_NAME):
    """Insert a new student after validating the input."""
    student_id = validate_non_empty(student_id, "Student ID")
    name = validate_non_empty(name, "Name")
    age = validate_age(age)
    email = validate_email(email)

    connection = connect(db_name)
    try:
        connection.execute(
            "INSERT INTO students (student_id, name, age, email) "
            "VALUES (?, ?, ?, ?)", (student_id, name, age, email))
        connection.commit()
    finally:
        connection.close()


def get_students(db_name=DB_NAME):
    """Return all the students as a list of rows."""
    connection = connect(db_name)
    rows = connection.execute("SELECT * FROM students ORDER BY student_id").fetchall()
    connection.close()
    return rows


def update_student(student_id, name, age, email, db_name=DB_NAME):
    """Update the details of an existing student."""
    name = validate_non_empty(name, "Name")
    age = validate_age(age)
    email = validate_email(email)

    connection = connect(db_name)
    connection.execute(
        "UPDATE students SET name = ?, age = ?, email = ? WHERE student_id = ?",
        (name, age, email, student_id))
    connection.commit()
    connection.close()


def delete_student(student_id, db_name=DB_NAME):
    """Delete a student and the related enrollments."""
    connection = connect(db_name)
    connection.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    connection.commit()
    connection.close()


# --------------------------------------------------------------------------
# CRUD: instructors
# --------------------------------------------------------------------------

def add_instructor(instructor_id, name, age, email, db_name=DB_NAME):
    """Insert a new instructor after validating the input."""
    instructor_id = validate_non_empty(instructor_id, "Instructor ID")
    name = validate_non_empty(name, "Name")
    age = validate_age(age)
    email = validate_email(email)

    connection = connect(db_name)
    try:
        connection.execute(
            "INSERT INTO instructors (instructor_id, name, age, email) "
            "VALUES (?, ?, ?, ?)", (instructor_id, name, age, email))
        connection.commit()
    finally:
        connection.close()


def get_instructors(db_name=DB_NAME):
    """Return all the instructors as a list of rows."""
    connection = connect(db_name)
    rows = connection.execute(
        "SELECT * FROM instructors ORDER BY instructor_id").fetchall()
    connection.close()
    return rows


def update_instructor(instructor_id, name, age, email, db_name=DB_NAME):
    """Update the details of an existing instructor."""
    name = validate_non_empty(name, "Name")
    age = validate_age(age)
    email = validate_email(email)

    connection = connect(db_name)
    connection.execute(
        "UPDATE instructors SET name = ?, age = ?, email = ? "
        "WHERE instructor_id = ?", (name, age, email, instructor_id))
    connection.commit()
    connection.close()


def delete_instructor(instructor_id, db_name=DB_NAME):
    """Delete an instructor; the taught courses keep no instructor."""
    connection = connect(db_name)
    connection.execute("DELETE FROM instructors WHERE instructor_id = ?",
                       (instructor_id,))
    connection.commit()
    connection.close()


# --------------------------------------------------------------------------
# CRUD: courses
# --------------------------------------------------------------------------

def add_course(course_id, course_name, instructor_id=None, db_name=DB_NAME):
    """Insert a new course, optionally already assigned to an instructor."""
    course_id = validate_non_empty(course_id, "Course ID")
    course_name = validate_non_empty(course_name, "Course name")

    connection = connect(db_name)
    try:
        connection.execute(
            "INSERT INTO courses (course_id, course_name, instructor_id) "
            "VALUES (?, ?, ?)", (course_id, course_name, instructor_id))
        connection.commit()
    finally:
        connection.close()


def get_courses(db_name=DB_NAME):
    """Return all the courses together with the instructor name."""
    connection = connect(db_name)
    rows = connection.execute("""
        SELECT c.course_id, c.course_name, c.instructor_id, i.name AS instructor_name
        FROM courses c
        LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
        ORDER BY c.course_id
    """).fetchall()
    connection.close()
    return rows


def update_course(course_id, course_name, instructor_id=None, db_name=DB_NAME):
    """Update the name and the instructor of an existing course."""
    course_name = validate_non_empty(course_name, "Course name")

    connection = connect(db_name)
    connection.execute(
        "UPDATE courses SET course_name = ?, instructor_id = ? WHERE course_id = ?",
        (course_name, instructor_id, course_id))
    connection.commit()
    connection.close()


def delete_course(course_id, db_name=DB_NAME):
    """Delete a course and the related enrollments."""
    connection = connect(db_name)
    connection.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
    connection.commit()
    connection.close()


def assign_instructor(course_id, instructor_id, db_name=DB_NAME):
    """Assign an instructor to a course."""
    connection = connect(db_name)
    connection.execute("UPDATE courses SET instructor_id = ? WHERE course_id = ?",
                       (instructor_id, course_id))
    connection.commit()
    connection.close()


# --------------------------------------------------------------------------
# CRUD: enrollments
# --------------------------------------------------------------------------

def register_student(student_id, course_id, db_name=DB_NAME):
    """Register a student in a course."""
    connection = connect(db_name)
    try:
        connection.execute(
            "INSERT OR IGNORE INTO enrollments (student_id, course_id) "
            "VALUES (?, ?)", (student_id, course_id))
        connection.commit()
    finally:
        connection.close()


def get_enrollments(db_name=DB_NAME):
    """Return all the enrollments with the student and course names."""
    connection = connect(db_name)
    rows = connection.execute("""
        SELECT e.student_id, s.name AS student_name,
               e.course_id, c.course_name
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses  c ON e.course_id  = c.course_id
        ORDER BY e.student_id
    """).fetchall()
    connection.close()
    return rows


def get_student_courses(student_id, db_name=DB_NAME):
    """Return the course IDs a student is registered in."""
    connection = connect(db_name)
    rows = connection.execute(
        "SELECT course_id FROM enrollments WHERE student_id = ?",
        (student_id,)).fetchall()
    connection.close()
    return [row["course_id"] for row in rows]


def unregister_student(student_id, course_id, db_name=DB_NAME):
    """Remove a student from a course."""
    connection = connect(db_name)
    connection.execute(
        "DELETE FROM enrollments WHERE student_id = ? AND course_id = ?",
        (student_id, course_id))
    connection.commit()
    connection.close()


# --------------------------------------------------------------------------
# Search
# --------------------------------------------------------------------------

def search_records(query, db_name=DB_NAME):
    """Search students, instructors and courses by name, ID or course."""
    pattern = "%" + query + "%"
    connection = connect(db_name)

    students = connection.execute("""
        SELECT DISTINCT s.* FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        WHERE s.name LIKE ? OR s.student_id LIKE ? OR e.course_id LIKE ?
    """, (pattern, pattern, pattern)).fetchall()

    instructors = connection.execute("""
        SELECT DISTINCT i.* FROM instructors i
        LEFT JOIN courses c ON i.instructor_id = c.instructor_id
        WHERE i.name LIKE ? OR i.instructor_id LIKE ? OR c.course_id LIKE ?
    """, (pattern, pattern, pattern)).fetchall()

    courses = connection.execute("""
        SELECT * FROM courses
        WHERE course_name LIKE ? OR course_id LIKE ?
    """, (pattern, pattern)).fetchall()

    connection.close()
    return students, instructors, courses


# --------------------------------------------------------------------------
# Backup and restore
# --------------------------------------------------------------------------

def backup_database(backup_path, db_name=DB_NAME):
    """Copy the database file to the given backup path."""
    if not os.path.exists(db_name):
        raise FileNotFoundError("Database file not found: " + db_name)
    shutil.copyfile(db_name, backup_path)
    return backup_path


def restore_database(backup_path, db_name=DB_NAME):
    """Restore the database from a backup file."""
    if not os.path.exists(backup_path):
        raise FileNotFoundError("Backup file not found: " + backup_path)
    shutil.copyfile(backup_path, db_name)
    return db_name


# --------------------------------------------------------------------------
# PyQt5 interface connected to the database
# --------------------------------------------------------------------------

class DatabaseWindow(QWidget):
    """PyQt5 window where every action reads from or writes to SQLite."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System - Database")
        self.resize(1000, 750)
        create_tables()

        layout = QVBoxLayout()
        layout.addLayout(self.build_forms())
        layout.addLayout(self.build_actions())
        layout.addLayout(self.build_search())
        layout.addWidget(self.build_table())
        self.setLayout(layout)

        self.refresh_all()

    # ------------------------------------------------------------------
    # Interface construction
    # ------------------------------------------------------------------

    def build_forms(self):
        """Build the student, instructor and course entry forms."""
        row = QHBoxLayout()

        student_box = QGroupBox("Add Student")
        student_layout = QGridLayout()
        self.student_id = QLineEdit()
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        for index, (label, field) in enumerate([("Student ID", self.student_id),
                                                ("Name", self.student_name),
                                                ("Age", self.student_age),
                                                ("Email", self.student_email)]):
            student_layout.addWidget(QLabel(label), index, 0)
            student_layout.addWidget(field, index, 1)
        button = QPushButton("Add Student")
        button.clicked.connect(self.on_add_student)
        student_layout.addWidget(button, 4, 0, 1, 2)
        student_box.setLayout(student_layout)
        row.addWidget(student_box)

        instructor_box = QGroupBox("Add Instructor")
        instructor_layout = QGridLayout()
        self.instructor_id = QLineEdit()
        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        for index, (label, field) in enumerate(
                [("Instructor ID", self.instructor_id),
                 ("Name", self.instructor_name),
                 ("Age", self.instructor_age),
                 ("Email", self.instructor_email)]):
            instructor_layout.addWidget(QLabel(label), index, 0)
            instructor_layout.addWidget(field, index, 1)
        button = QPushButton("Add Instructor")
        button.clicked.connect(self.on_add_instructor)
        instructor_layout.addWidget(button, 4, 0, 1, 2)
        instructor_box.setLayout(instructor_layout)
        row.addWidget(instructor_box)

        course_box = QGroupBox("Add Course")
        course_layout = QGridLayout()
        self.course_id = QLineEdit()
        self.course_name = QLineEdit()
        course_layout.addWidget(QLabel("Course ID"), 0, 0)
        course_layout.addWidget(self.course_id, 0, 1)
        course_layout.addWidget(QLabel("Course Name"), 1, 0)
        course_layout.addWidget(self.course_name, 1, 1)
        button = QPushButton("Add Course")
        button.clicked.connect(self.on_add_course)
        course_layout.addWidget(button, 2, 0, 1, 2)
        course_box.setLayout(course_layout)
        row.addWidget(course_box)

        return row

    def build_actions(self):
        """Build the registration, assignment and backup groups."""
        row = QHBoxLayout()

        register_box = QGroupBox("Student Registration")
        register_layout = QGridLayout()
        self.register_student_box = QComboBox()
        self.register_course_box = QComboBox()
        register_layout.addWidget(QLabel("Student"), 0, 0)
        register_layout.addWidget(self.register_student_box, 0, 1)
        register_layout.addWidget(QLabel("Course"), 1, 0)
        register_layout.addWidget(self.register_course_box, 1, 1)
        button = QPushButton("Register Course")
        button.clicked.connect(self.on_register_student)
        register_layout.addWidget(button, 2, 0, 1, 2)
        register_box.setLayout(register_layout)
        row.addWidget(register_box)

        assign_box = QGroupBox("Instructor Assignment")
        assign_layout = QGridLayout()
        self.assign_instructor_box = QComboBox()
        self.assign_course_box = QComboBox()
        assign_layout.addWidget(QLabel("Instructor"), 0, 0)
        assign_layout.addWidget(self.assign_instructor_box, 0, 1)
        assign_layout.addWidget(QLabel("Course"), 1, 0)
        assign_layout.addWidget(self.assign_course_box, 1, 1)
        button = QPushButton("Assign Course")
        button.clicked.connect(self.on_assign_instructor)
        assign_layout.addWidget(button, 2, 0, 1, 2)
        assign_box.setLayout(assign_layout)
        row.addWidget(assign_box)

        backup_box = QGroupBox("Database")
        backup_layout = QVBoxLayout()
        for text, handler in [("Backup Database", self.on_backup),
                              ("Restore Database", self.on_restore)]:
            button = QPushButton(text)
            button.clicked.connect(handler)
            backup_layout.addWidget(button)
        backup_box.setLayout(backup_layout)
        row.addWidget(backup_box)

        return row

    def build_search(self):
        """Build the search bar and the edit/delete buttons."""
        row = QHBoxLayout()
        row.addWidget(QLabel("Search (name, ID or course):"))
        self.search_field = QLineEdit()
        self.search_field.textChanged.connect(self.refresh_table)
        row.addWidget(self.search_field)

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.on_edit_selected)
        row.addWidget(edit_button)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.on_delete_selected)
        row.addWidget(delete_button)

        return row

    def build_table(self):
        """Build the QTableWidget that displays the database records."""
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Type", "ID", "Name", "Age", "Email", "Courses / Instructor"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return self.table

    @staticmethod
    def parse_id(value):
        """Return the ID part of an 'ID - Name' dropdown entry."""
        return value.split(" - ")[0] if value else ""

    # ------------------------------------------------------------------
    # Create operations
    # ------------------------------------------------------------------

    def on_add_student(self):
        try:
            add_student(self.student_id.text(), self.student_name.text(),
                        self.student_age.text(), self.student_email.text())
        except ValueError as error:
            QMessageBox.critical(self, "Invalid input", str(error))
            return
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Database error",
                                 "A student with this ID already exists")
            return

        for field in (self.student_id, self.student_name, self.student_age,
                      self.student_email):
            field.clear()
        self.refresh_all()

    def on_add_instructor(self):
        try:
            add_instructor(self.instructor_id.text(), self.instructor_name.text(),
                           self.instructor_age.text(),
                           self.instructor_email.text())
        except ValueError as error:
            QMessageBox.critical(self, "Invalid input", str(error))
            return
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Database error",
                                 "An instructor with this ID already exists")
            return

        for field in (self.instructor_id, self.instructor_name,
                      self.instructor_age, self.instructor_email):
            field.clear()
        self.refresh_all()

    def on_add_course(self):
        try:
            add_course(self.course_id.text(), self.course_name.text())
        except ValueError as error:
            QMessageBox.critical(self, "Invalid input", str(error))
            return
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Database error",
                                 "A course with this ID already exists")
            return

        self.course_id.clear()
        self.course_name.clear()
        self.refresh_all()

    def on_register_student(self):
        student_id = self.parse_id(self.register_student_box.currentText())
        course_id = self.parse_id(self.register_course_box.currentText())
        if not student_id or not course_id:
            QMessageBox.warning(self, "Missing selection",
                                "Select both a student and a course")
            return
        register_student(student_id, course_id)
        self.refresh_all()

    def on_assign_instructor(self):
        instructor_id = self.parse_id(self.assign_instructor_box.currentText())
        course_id = self.parse_id(self.assign_course_box.currentText())
        if not instructor_id or not course_id:
            QMessageBox.warning(self, "Missing selection",
                                "Select both an instructor and a course")
            return
        assign_instructor(course_id, instructor_id)
        self.refresh_all()

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def refresh_all(self):
        """Reload the dropdowns and the table from the database."""
        students = get_students()
        instructors = get_instructors()
        courses = get_courses()

        self.register_student_box.clear()
        self.register_student_box.addItems(
            [f"{s['student_id']} - {s['name']}" for s in students])
        self.assign_instructor_box.clear()
        self.assign_instructor_box.addItems(
            [f"{i['instructor_id']} - {i['name']}" for i in instructors])
        course_values = [f"{c['course_id']} - {c['course_name']}" for c in courses]
        self.register_course_box.clear()
        self.register_course_box.addItems(course_values)
        self.assign_course_box.clear()
        self.assign_course_box.addItems(course_values)

        self.refresh_table()

    def refresh_table(self):
        """Fill the table with the database records matching the search."""
        query = self.search_field.text().strip()
        if query:
            students, instructors, courses = search_records(query)
            course_rows = [dict(c) for c in courses]
            for course in course_rows:
                course["instructor_name"] = None
            for full in get_courses():
                for course in course_rows:
                    if course["course_id"] == full["course_id"]:
                        course["instructor_name"] = full["instructor_name"]
        else:
            students = get_students()
            instructors = get_instructors()
            course_rows = [dict(c) for c in get_courses()]

        rows = []
        for student in students:
            courses_text = ", ".join(get_student_courses(student["student_id"]))
            rows.append(["Student", student["student_id"], student["name"],
                         str(student["age"]), student["email"], courses_text])

        taught = {}
        for course in get_courses():
            if course["instructor_id"]:
                taught.setdefault(course["instructor_id"], []).append(
                    course["course_id"])
        for instructor in instructors:
            courses_text = ", ".join(taught.get(instructor["instructor_id"], []))
            rows.append(["Instructor", instructor["instructor_id"],
                         instructor["name"], str(instructor["age"]),
                         instructor["email"], courses_text])

        for course in course_rows:
            rows.append(["Course", course["course_id"], course["course_name"],
                         "", "", course["instructor_name"] or "-"])

        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                self.table.setItem(row_index, column_index,
                                   QTableWidgetItem(value))

    # ------------------------------------------------------------------
    # Update and delete operations
    # ------------------------------------------------------------------

    def selected_record(self):
        """Return the (type, id) of the selected row, or (None, None)."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "No selection", "Select a record first")
            return None, None
        return self.table.item(row, 0).text(), self.table.item(row, 1).text()

    def on_delete_selected(self):
        record_type, record_id = self.selected_record()
        if not record_type:
            return
        confirm = QMessageBox.question(self, "Confirm",
                                       f"Delete {record_type} {record_id}?")
        if confirm != QMessageBox.Yes:
            return

        if record_type == "Student":
            delete_student(record_id)
        elif record_type == "Instructor":
            delete_instructor(record_id)
        else:
            delete_course(record_id)
        self.refresh_all()

    def on_edit_selected(self):
        """Open a dialog to update the selected database record."""
        record_type, record_id = self.selected_record()
        if not record_type:
            return

        row = self.table.currentRow()
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit " + record_type)
        form = QFormLayout()
        fields = {}

        if record_type == "Course":
            fields["Course Name"] = QLineEdit(self.table.item(row, 2).text())
        else:
            fields["Name"] = QLineEdit(self.table.item(row, 2).text())
            fields["Age"] = QLineEdit(self.table.item(row, 3).text())
            fields["Email"] = QLineEdit(self.table.item(row, 4).text())

        for label, field in fields.items():
            form.addRow(label, field)

        def save_changes():
            try:
                if record_type == "Course":
                    update_course(record_id, fields["Course Name"].text(),
                                  self.course_instructor_id(record_id))
                elif record_type == "Student":
                    update_student(record_id, fields["Name"].text(),
                                   fields["Age"].text(), fields["Email"].text())
                else:
                    update_instructor(record_id, fields["Name"].text(),
                                      fields["Age"].text(), fields["Email"].text())
            except ValueError as error:
                QMessageBox.critical(dialog, "Invalid input", str(error))
                return
            dialog.accept()
            self.refresh_all()

        save_button = QPushButton("Save")
        save_button.clicked.connect(save_changes)
        form.addRow(save_button)
        dialog.setLayout(form)
        dialog.exec_()

    @staticmethod
    def course_instructor_id(course_id):
        """Return the instructor currently assigned to a course."""
        for course in get_courses():
            if course["course_id"] == course_id:
                return course["instructor_id"]
        return None

    # ------------------------------------------------------------------
    # Backup and restore
    # ------------------------------------------------------------------

    def on_backup(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Backup Database", "",
                                                  "Database files (*.db)")
        if not filename:
            return
        try:
            backup_database(filename)
        except OSError as error:
            QMessageBox.critical(self, "Backup failed", str(error))
            return
        QMessageBox.information(self, "Backup", "Database backed up to " + filename)

    def on_restore(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Restore Database", "",
                                                  "Database files (*.db)")
        if not filename:
            return
        try:
            restore_database(filename)
        except OSError as error:
            QMessageBox.critical(self, "Restore failed", str(error))
            return
        self.refresh_all()
        QMessageBox.information(self, "Restore",
                                "Database restored from " + filename)


# --------------------------------------------------------------------------
# Demonstration
# --------------------------------------------------------------------------

def run_demo():
    """Run the CRUD, search and backup operations from the console."""
    create_tables()

    # Start from a clean state so the demo can be run several times.
    connection = connect()
    for table in ("enrollments", "courses", "students", "instructors"):
        connection.execute("DELETE FROM " + table)
    connection.commit()
    connection.close()

    add_student("S001", "Sample Student", 21, "student1@example.com")
    add_student("S002", "Sample Student Two", 22, "student2@example.com")
    add_instructor("I001", "Sample Instructor", 45, "instructor@example.com")
    add_course("EECE435L", "Software Tools Lab")

    assign_instructor("EECE435L", "I001")
    register_student("S001", "EECE435L")
    register_student("S002", "EECE435L")

    print("Students:")
    for row in get_students():
        print(" ", dict(row))

    print("Instructors:")
    for row in get_instructors():
        print(" ", dict(row))

    print("Courses:")
    for row in get_courses():
        print(" ", dict(row))

    print("Enrollments:")
    for row in get_enrollments():
        print(" ", dict(row))

    update_student("S002", "Sample Student Two", 23, "student2@example.com")
    delete_student("S001")
    print("After update and delete:")
    for row in get_students():
        print(" ", dict(row))

    students, instructors, courses = search_records("EECE")
    print(f"Search 'EECE': {len(students)} student(s), "
          f"{len(instructors)} instructor(s), {len(courses)} course(s)")

    print("Backup created at:", backup_database("435Ldb_backup.db"))


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        app = QApplication(sys.argv)
        window = DatabaseWindow()
        window.show()
        sys.exit(app.exec_())
