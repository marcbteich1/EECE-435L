"""Part 3: GUI with PyQt5 - School Management System.

Forms built with QLineEdit, registration and assignment through
QComboBox dropdowns, records shown in a QTableWidget with search,
edit/delete, save/load and CSV export.
"""

import csv
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QComboBox, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QGroupBox, QMessageBox, QFileDialog,
                             QDialog, QFormLayout, QHeaderView)

from part1_oop import (Student, Instructor, Course, save_data, load_data,
                       validate_email, validate_age, validate_non_empty)


class SchoolManagementWindow(QWidget):
    """Main PyQt5 window of the school management system."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.resize(1000, 750)

        self.students = []
        self.instructors = []
        self.courses = []

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

        # --- Student form ---
        student_box = QGroupBox("Add Student")
        student_layout = QGridLayout()
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()
        for index, (label, field) in enumerate([("Name", self.student_name),
                                                ("Age", self.student_age),
                                                ("Email", self.student_email),
                                                ("Student ID", self.student_id)]):
            student_layout.addWidget(QLabel(label), index, 0)
            student_layout.addWidget(field, index, 1)
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        student_layout.addWidget(add_student_button, 4, 0, 1, 2)
        student_box.setLayout(student_layout)
        row.addWidget(student_box)

        # --- Instructor form ---
        instructor_box = QGroupBox("Add Instructor")
        instructor_layout = QGridLayout()
        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()
        for index, (label, field) in enumerate(
                [("Name", self.instructor_name), ("Age", self.instructor_age),
                 ("Email", self.instructor_email),
                 ("Instructor ID", self.instructor_id)]):
            instructor_layout.addWidget(QLabel(label), index, 0)
            instructor_layout.addWidget(field, index, 1)
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)
        instructor_layout.addWidget(add_instructor_button, 4, 0, 1, 2)
        instructor_box.setLayout(instructor_layout)
        row.addWidget(instructor_box)

        # --- Course form ---
        course_box = QGroupBox("Add Course")
        course_layout = QGridLayout()
        self.course_id = QLineEdit()
        self.course_name = QLineEdit()
        course_layout.addWidget(QLabel("Course ID"), 0, 0)
        course_layout.addWidget(self.course_id, 0, 1)
        course_layout.addWidget(QLabel("Course Name"), 1, 0)
        course_layout.addWidget(self.course_name, 1, 1)
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        course_layout.addWidget(add_course_button, 2, 0, 1, 2)
        course_box.setLayout(course_layout)
        row.addWidget(course_box)

        return row

    def build_actions(self):
        """Build the registration, assignment and file action groups."""
        row = QHBoxLayout()

        # --- Student registration ---
        register_box = QGroupBox("Student Registration")
        register_layout = QGridLayout()
        self.register_student_box = QComboBox()
        self.register_course_box = QComboBox()
        register_layout.addWidget(QLabel("Student"), 0, 0)
        register_layout.addWidget(self.register_student_box, 0, 1)
        register_layout.addWidget(QLabel("Course"), 1, 0)
        register_layout.addWidget(self.register_course_box, 1, 1)
        register_button = QPushButton("Register Course")
        register_button.clicked.connect(self.register_course)
        register_layout.addWidget(register_button, 2, 0, 1, 2)
        register_box.setLayout(register_layout)
        row.addWidget(register_box)

        # --- Instructor assignment ---
        assign_box = QGroupBox("Instructor Assignment")
        assign_layout = QGridLayout()
        self.assign_instructor_box = QComboBox()
        self.assign_course_box = QComboBox()
        assign_layout.addWidget(QLabel("Instructor"), 0, 0)
        assign_layout.addWidget(self.assign_instructor_box, 0, 1)
        assign_layout.addWidget(QLabel("Course"), 1, 0)
        assign_layout.addWidget(self.assign_course_box, 1, 1)
        assign_button = QPushButton("Assign Course")
        assign_button.clicked.connect(self.assign_course)
        assign_layout.addWidget(assign_button, 2, 0, 1, 2)
        assign_box.setLayout(assign_layout)
        row.addWidget(assign_box)

        # --- File actions ---
        file_box = QGroupBox("Data")
        file_layout = QVBoxLayout()
        for text, handler in [("Save Data", self.save_to_file),
                              ("Load Data", self.load_from_file),
                              ("Export to CSV", self.export_to_csv)]:
            button = QPushButton(text)
            button.clicked.connect(handler)
            file_layout.addWidget(button)
        file_box.setLayout(file_layout)
        row.addWidget(file_box)

        return row

    def build_search(self):
        """Build the search bar and the edit/delete buttons."""
        row = QHBoxLayout()
        row.addWidget(QLabel("Search (name, ID or course):"))
        self.search_field = QLineEdit()
        self.search_field.textChanged.connect(self.refresh_table)
        row.addWidget(self.search_field)

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_selected)
        row.addWidget(edit_button)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected)
        row.addWidget(delete_button)

        return row

    def build_table(self):
        """Build the QTableWidget that displays all the records."""
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Type", "ID", "Name", "Age", "Email", "Courses / Instructor"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return self.table

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_instructor(self, instructor_id):
        for instructor in self.instructors:
            if instructor.instructor_id == instructor_id:
                return instructor
        return None

    def find_course(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    @staticmethod
    def parse_id(value):
        """Return the ID part of an 'ID - Name' dropdown entry."""
        return value.split(" - ")[0] if value else ""

    # ------------------------------------------------------------------
    # Adding records
    # ------------------------------------------------------------------

    def add_student(self):
        try:
            name = validate_non_empty(self.student_name.text(), "Name")
            age = validate_age(self.student_age.text())
            email = validate_email(self.student_email.text())
            student_id = validate_non_empty(self.student_id.text(), "Student ID")
            if self.find_student(student_id):
                raise ValueError("A student with this ID already exists")
            self.students.append(Student(name, age, email, student_id))
        except ValueError as error:
            QMessageBox.critical(self, "Invalid input", str(error))
            return

        for field in (self.student_name, self.student_age, self.student_email,
                      self.student_id):
            field.clear()
        self.refresh_all()

    def add_instructor(self):
        try:
            name = validate_non_empty(self.instructor_name.text(), "Name")
            age = validate_age(self.instructor_age.text())
            email = validate_email(self.instructor_email.text())
            instructor_id = validate_non_empty(self.instructor_id.text(),
                                               "Instructor ID")
            if self.find_instructor(instructor_id):
                raise ValueError("An instructor with this ID already exists")
            self.instructors.append(Instructor(name, age, email, instructor_id))
        except ValueError as error:
            QMessageBox.critical(self, "Invalid input", str(error))
            return

        for field in (self.instructor_name, self.instructor_age,
                      self.instructor_email, self.instructor_id):
            field.clear()
        self.refresh_all()

    def add_course(self):
        try:
            course_id = validate_non_empty(self.course_id.text(), "Course ID")
            course_name = validate_non_empty(self.course_name.text(),
                                             "Course name")
            if self.find_course(course_id):
                raise ValueError("A course with this ID already exists")
            self.courses.append(Course(course_id, course_name))
        except ValueError as error:
            QMessageBox.critical(self, "Invalid input", str(error))
            return

        self.course_id.clear()
        self.course_name.clear()
        self.refresh_all()

    # ------------------------------------------------------------------
    # Registration and assignment
    # ------------------------------------------------------------------

    def register_course(self):
        student = self.find_student(
            self.parse_id(self.register_student_box.currentText()))
        course = self.find_course(
            self.parse_id(self.register_course_box.currentText()))
        if not student or not course:
            QMessageBox.warning(self, "Missing selection",
                                "Select both a student and a course")
            return
        student.register_course(course)
        self.refresh_all()

    def assign_course(self):
        instructor = self.find_instructor(
            self.parse_id(self.assign_instructor_box.currentText()))
        course = self.find_course(
            self.parse_id(self.assign_course_box.currentText()))
        if not instructor or not course:
            QMessageBox.warning(self, "Missing selection",
                                "Select both an instructor and a course")
            return
        instructor.assign_course(course)
        self.refresh_all()

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def refresh_all(self):
        """Refresh the dropdowns and the table."""
        self.register_student_box.clear()
        self.register_student_box.addItems(
            [f"{s.student_id} - {s.name}" for s in self.students])
        self.assign_instructor_box.clear()
        self.assign_instructor_box.addItems(
            [f"{i.instructor_id} - {i.name}" for i in self.instructors])
        course_values = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.register_course_box.clear()
        self.register_course_box.addItems(course_values)
        self.assign_course_box.clear()
        self.assign_course_box.addItems(course_values)
        self.refresh_table()

    def collect_rows(self):
        """Return the rows to display, filtered by the search query."""
        query = self.search_field.text().strip().lower()
        rows = []

        for student in self.students:
            courses = ", ".join(c.course_id for c in student.registered_courses)
            if self.matches(query, student.name, student.student_id, courses):
                rows.append(["Student", student.student_id, student.name,
                             str(student.age), student.get_email(), courses])

        for instructor in self.instructors:
            courses = ", ".join(c.course_id for c in instructor.assigned_courses)
            if self.matches(query, instructor.name, instructor.instructor_id,
                            courses):
                rows.append(["Instructor", instructor.instructor_id,
                             instructor.name, str(instructor.age),
                             instructor.get_email(), courses])

        for course in self.courses:
            instructor_name = course.instructor.name if course.instructor else "-"
            if self.matches(query, course.course_name, course.course_id,
                            course.course_id):
                rows.append(["Course", course.course_id, course.course_name,
                             "", "", instructor_name])

        return rows

    def refresh_table(self):
        """Fill the QTableWidget with the current rows."""
        rows = self.collect_rows()
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                self.table.setItem(row_index, column_index,
                                   QTableWidgetItem(value))

    @staticmethod
    def matches(query, name, record_id, courses):
        """Return True if the record matches the search query."""
        if not query:
            return True
        return (query in name.lower() or query in record_id.lower()
                or query in courses.lower())

    # ------------------------------------------------------------------
    # Edit and delete
    # ------------------------------------------------------------------

    def selected_record(self):
        """Return the (type, id) of the selected row, or (None, None)."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "No selection", "Select a record first")
            return None, None
        return self.table.item(row, 0).text(), self.table.item(row, 1).text()

    def delete_selected(self):
        record_type, record_id = self.selected_record()
        if not record_type:
            return
        confirm = QMessageBox.question(self, "Confirm",
                                       f"Delete {record_type} {record_id}?")
        if confirm != QMessageBox.Yes:
            return

        if record_type == "Student":
            student = self.find_student(record_id)
            for course in student.registered_courses:
                if student in course.enrolled_students:
                    course.enrolled_students.remove(student)
            self.students.remove(student)
        elif record_type == "Instructor":
            instructor = self.find_instructor(record_id)
            for course in instructor.assigned_courses:
                if course.instructor is instructor:
                    course.instructor = None
            self.instructors.remove(instructor)
        else:
            course = self.find_course(record_id)
            for student in course.enrolled_students:
                if course in student.registered_courses:
                    student.registered_courses.remove(course)
            if course.instructor and course in course.instructor.assigned_courses:
                course.instructor.assigned_courses.remove(course)
            self.courses.remove(course)

        self.refresh_all()

    def edit_selected(self):
        """Open a dialog to edit the selected record."""
        record_type, record_id = self.selected_record()
        if not record_type:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit " + record_type)
        form = QFormLayout()
        fields = {}

        if record_type == "Course":
            course = self.find_course(record_id)
            fields["Course Name"] = QLineEdit(course.course_name)
        else:
            person = (self.find_student(record_id) if record_type == "Student"
                      else self.find_instructor(record_id))
            fields["Name"] = QLineEdit(person.name)
            fields["Age"] = QLineEdit(str(person.age))
            fields["Email"] = QLineEdit(person.get_email())

        for label, field in fields.items():
            form.addRow(label, field)

        def save_changes():
            try:
                if record_type == "Course":
                    course.course_name = validate_non_empty(
                        fields["Course Name"].text(), "Course name")
                else:
                    person.name = validate_non_empty(fields["Name"].text(), "Name")
                    person.age = validate_age(fields["Age"].text())
                    person.set_email(fields["Email"].text())
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

    # ------------------------------------------------------------------
    # Save, load and export
    # ------------------------------------------------------------------

    def save_to_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "",
                                                  "JSON files (*.json)")
        if not filename:
            return
        save_data(filename, self.students, self.instructors, self.courses)
        QMessageBox.information(self, "Saved", "Data saved to " + filename)

    def load_from_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "",
                                                  "JSON files (*.json)")
        if not filename:
            return
        try:
            self.students, self.instructors, self.courses = load_data(filename)
        except (OSError, ValueError, KeyError) as error:
            QMessageBox.critical(self, "Load failed", str(error))
            return
        self.refresh_all()
        QMessageBox.information(self, "Loaded", "Data loaded from " + filename)

    def export_to_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "",
                                                  "CSV files (*.csv)")
        if not filename:
            return
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "ID", "Name", "Age", "Email",
                             "Courses / Instructor"])
            writer.writerows(self.collect_rows())
        QMessageBox.information(self, "Exported", "Records exported to " + filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementWindow()
    window.show()
    sys.exit(app.exec_())
