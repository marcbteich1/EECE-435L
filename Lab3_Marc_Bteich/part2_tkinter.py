"""Part 2: GUI with Tkinter - School Management System.

Forms to add students, instructors and courses, course registration and
instructor assignment through dropdowns, a Treeview showing all records,
search, edit/delete and save/load to a JSON file.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from part1_oop import (Student, Instructor, Course, save_data, load_data,
                       validate_email, validate_age, validate_non_empty)


class SchoolManagementApp:
    """Manage students, instructors and courses through a Tkinter interface.

    :param root: Main window used to display the application.
    :type root: tkinter.Tk
    :ivar root: Application window.
    :vartype root: tkinter.Tk
    :ivar students: Current student records.
    :vartype students: list[part1_oop.Student]
    :ivar instructors: Current instructor records.
    :vartype instructors: list[part1_oop.Instructor]
    :ivar courses: Current course records.
    :vartype courses: list[part1_oop.Course]
    """

    def __init__(self, root):
        """Initialize the records and build the application interface.
        
        :param root: Main Tkinter window.
        :type root: tkinter.Tk
        """
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("950x700")

        self.students = []
        self.instructors = []
        self.courses = []

        self.build_forms()
        self.build_actions()
        self.build_search()
        self.build_table()
        self.refresh_all()

    # ------------------------------------------------------------------
    # Interface construction
    # ------------------------------------------------------------------

    def build_forms(self):
        """Build the three entry forms (student, instructor, course).
        
        :return: None.
        :rtype: None
        """
        forms = tk.Frame(self.root)
        forms.pack(fill="x", padx=10, pady=10)

        # --- Student form ---
        student_frame = tk.LabelFrame(forms, text="Add Student", padx=5, pady=5)
        student_frame.grid(row=0, column=0, padx=5, sticky="n")

        tk.Label(student_frame, text="Name").grid(row=0, column=0, sticky="e")
        self.student_name = tk.Entry(student_frame)
        self.student_name.grid(row=0, column=1)

        tk.Label(student_frame, text="Age").grid(row=1, column=0, sticky="e")
        self.student_age = tk.Entry(student_frame)
        self.student_age.grid(row=1, column=1)

        tk.Label(student_frame, text="Email").grid(row=2, column=0, sticky="e")
        self.student_email = tk.Entry(student_frame)
        self.student_email.grid(row=2, column=1)

        tk.Label(student_frame, text="Student ID").grid(row=3, column=0, sticky="e")
        self.student_id = tk.Entry(student_frame)
        self.student_id.grid(row=3, column=1)

        tk.Button(student_frame, text="Add Student",
                  command=self.add_student).grid(row=4, column=0, columnspan=2,
                                                 pady=5, sticky="ew")

        # --- Instructor form ---
        instructor_frame = tk.LabelFrame(forms, text="Add Instructor",
                                         padx=5, pady=5)
        instructor_frame.grid(row=0, column=1, padx=5, sticky="n")

        tk.Label(instructor_frame, text="Name").grid(row=0, column=0, sticky="e")
        self.instructor_name = tk.Entry(instructor_frame)
        self.instructor_name.grid(row=0, column=1)

        tk.Label(instructor_frame, text="Age").grid(row=1, column=0, sticky="e")
        self.instructor_age = tk.Entry(instructor_frame)
        self.instructor_age.grid(row=1, column=1)

        tk.Label(instructor_frame, text="Email").grid(row=2, column=0, sticky="e")
        self.instructor_email = tk.Entry(instructor_frame)
        self.instructor_email.grid(row=2, column=1)

        tk.Label(instructor_frame, text="Instructor ID").grid(row=3, column=0,
                                                              sticky="e")
        self.instructor_id = tk.Entry(instructor_frame)
        self.instructor_id.grid(row=3, column=1)

        tk.Button(instructor_frame, text="Add Instructor",
                  command=self.add_instructor).grid(row=4, column=0, columnspan=2,
                                                    pady=5, sticky="ew")

        # --- Course form ---
        course_frame = tk.LabelFrame(forms, text="Add Course", padx=5, pady=5)
        course_frame.grid(row=0, column=2, padx=5, sticky="n")

        tk.Label(course_frame, text="Course ID").grid(row=0, column=0, sticky="e")
        self.course_id = tk.Entry(course_frame)
        self.course_id.grid(row=0, column=1)

        tk.Label(course_frame, text="Course Name").grid(row=1, column=0, sticky="e")
        self.course_name = tk.Entry(course_frame)
        self.course_name.grid(row=1, column=1)

        tk.Button(course_frame, text="Add Course",
                  command=self.add_course).grid(row=2, column=0, columnspan=2,
                                                pady=5, sticky="ew")

    def build_actions(self):
        """Build the registration and assignment dropdowns.
        
        :return: None.
        :rtype: None
        """
        actions = tk.Frame(self.root)
        actions.pack(fill="x", padx=10)

        # --- Student registration ---
        register_frame = tk.LabelFrame(actions, text="Student Registration",
                                       padx=5, pady=5)
        register_frame.grid(row=0, column=0, padx=5, sticky="n")

        tk.Label(register_frame, text="Student").grid(row=0, column=0, sticky="e")
        self.register_student_box = ttk.Combobox(register_frame, state="readonly",
                                                 width=25)
        self.register_student_box.grid(row=0, column=1)

        tk.Label(register_frame, text="Course").grid(row=1, column=0, sticky="e")
        self.register_course_box = ttk.Combobox(register_frame, state="readonly",
                                                width=25)
        self.register_course_box.grid(row=1, column=1)

        tk.Button(register_frame, text="Register Course",
                  command=self.register_course).grid(row=2, column=0, columnspan=2,
                                                     pady=5, sticky="ew")

        # --- Instructor assignment ---
        assign_frame = tk.LabelFrame(actions, text="Instructor Assignment",
                                     padx=5, pady=5)
        assign_frame.grid(row=0, column=1, padx=5, sticky="n")

        tk.Label(assign_frame, text="Instructor").grid(row=0, column=0, sticky="e")
        self.assign_instructor_box = ttk.Combobox(assign_frame, state="readonly",
                                                  width=25)
        self.assign_instructor_box.grid(row=0, column=1)

        tk.Label(assign_frame, text="Course").grid(row=1, column=0, sticky="e")
        self.assign_course_box = ttk.Combobox(assign_frame, state="readonly",
                                              width=25)
        self.assign_course_box.grid(row=1, column=1)

        tk.Button(assign_frame, text="Assign Course",
                  command=self.assign_course).grid(row=2, column=0, columnspan=2,
                                                   pady=5, sticky="ew")

        # --- File actions ---
        file_frame = tk.LabelFrame(actions, text="Data", padx=5, pady=5)
        file_frame.grid(row=0, column=2, padx=5, sticky="n")

        tk.Button(file_frame, text="Save Data",
                  command=self.save_to_file).pack(fill="x", pady=2)
        tk.Button(file_frame, text="Load Data",
                  command=self.load_from_file).pack(fill="x", pady=2)

    def build_search(self):
        """Build the search bar and the edit/delete buttons.
        
        :return: None.
        :rtype: None
        """
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(search_frame, text="Search (name, ID or course):").pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search",
                  command=self.refresh_table).pack(side="left")
        tk.Button(search_frame, text="Clear",
                  command=self.clear_search).pack(side="left", padx=5)

        tk.Button(search_frame, text="Delete Selected",
                  command=self.delete_selected).pack(side="right", padx=5)
        tk.Button(search_frame, text="Edit Selected",
                  command=self.edit_selected).pack(side="right")

    def build_table(self):
        """Build the Treeview that displays all the records.
        
        :return: None.
        :rtype: None
        """
        columns = ("type", "id", "name", "age", "email", "extra")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        headings = {
            "type": "Type",
            "id": "ID",
            "name": "Name",
            "age": "Age",
            "email": "Email",
            "extra": "Courses / Instructor",
        }
        for column, heading in headings.items():
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=140)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------

    def find_student(self, student_id):
        """Find a student by ID.
        
        :param student_id: Student ID to look up.
        :type student_id: str
        :return: Matching student, or None if not found.
        :rtype: part1_oop.Student or None
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_instructor(self, instructor_id):
        """Find an instructor by ID.
        
        :param instructor_id: Instructor ID to look up.
        :type instructor_id: str
        :return: Matching instructor, or None if not found.
        :rtype: part1_oop.Instructor or None
        """
        for instructor in self.instructors:
            if instructor.instructor_id == instructor_id:
                return instructor
        return None

    def find_course(self, course_id):
        """Find a course by ID.
        
        :param course_id: Course ID to look up.
        :type course_id: str
        :return: Matching course, or None if not found.
        :rtype: part1_oop.Course or None
        """
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    @staticmethod
    def parse_id(value):
        """Extract the ID from an ``ID - Name`` dropdown entry.
        
        :param value: Selected dropdown text.
        :type value: str
        :return: ID portion, or an empty string for an empty selection.
        :rtype: str
        """
        return value.split(" - ")[0] if value else ""

    # ------------------------------------------------------------------
    # Adding records
    # ------------------------------------------------------------------

    def add_student(self):
        """Validate the student form, add the student and refresh the interface.
        
        Display an error dialog if input is invalid or the ID already exists.
        
        :return: None.
        :rtype: None
        """
        try:
            name = validate_non_empty(self.student_name.get(), "Name")
            age = validate_age(self.student_age.get())
            email = validate_email(self.student_email.get())
            student_id = validate_non_empty(self.student_id.get(), "Student ID")
            if self.find_student(student_id):
                raise ValueError("A student with this ID already exists")
            self.students.append(Student(name, age, email, student_id))
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        for entry in (self.student_name, self.student_age, self.student_email,
                      self.student_id):
            entry.delete(0, tk.END)
        self.refresh_all()

    def add_instructor(self):
        """Validate the instructor form, add the instructor and refresh the interface.
        
        Display an error dialog if input is invalid or the ID already exists.
        
        :return: None.
        :rtype: None
        """
        try:
            name = validate_non_empty(self.instructor_name.get(), "Name")
            age = validate_age(self.instructor_age.get())
            email = validate_email(self.instructor_email.get())
            instructor_id = validate_non_empty(self.instructor_id.get(),
                                               "Instructor ID")
            if self.find_instructor(instructor_id):
                raise ValueError("An instructor with this ID already exists")
            self.instructors.append(Instructor(name, age, email, instructor_id))
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        for entry in (self.instructor_name, self.instructor_age,
                      self.instructor_email, self.instructor_id):
            entry.delete(0, tk.END)
        self.refresh_all()

    def add_course(self):
        """Validate the course form, add the course and refresh the interface.
        
        Display an error dialog if input is invalid or the ID already exists.
        
        :return: None.
        :rtype: None
        """
        try:
            course_id = validate_non_empty(self.course_id.get(), "Course ID")
            course_name = validate_non_empty(self.course_name.get(), "Course name")
            if self.find_course(course_id):
                raise ValueError("A course with this ID already exists")
            self.courses.append(Course(course_id, course_name))
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        self.course_id.delete(0, tk.END)
        self.course_name.delete(0, tk.END)
        self.refresh_all()

    # ------------------------------------------------------------------
    # Registration and assignment
    # ------------------------------------------------------------------

    def register_course(self):
        """Register the selected student in the selected course.
        
        Display an error dialog if either selection is missing; otherwise refresh the interface.
        
        :return: None.
        :rtype: None
        """
        student = self.find_student(self.parse_id(self.register_student_box.get()))
        course = self.find_course(self.parse_id(self.register_course_box.get()))
        if not student or not course:
            messagebox.showerror("Missing selection",
                                 "Select both a student and a course")
            return
        student.register_course(course)
        self.refresh_all()

    def assign_course(self):
        """Assign the selected instructor to the selected course.
        
        Display an error dialog if either selection is missing; otherwise refresh the interface.
        
        :return: None.
        :rtype: None
        """
        instructor = self.find_instructor(
            self.parse_id(self.assign_instructor_box.get()))
        course = self.find_course(self.parse_id(self.assign_course_box.get()))
        if not instructor or not course:
            messagebox.showerror("Missing selection",
                                 "Select both an instructor and a course")
            return
        instructor.assign_course(course)
        self.refresh_all()

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def clear_search(self):
        """Clear the search field and display all records.
        
        :return: None.
        :rtype: None
        """
        self.search_entry.delete(0, tk.END)
        self.refresh_table()

    def refresh_all(self):
        """Refresh the dropdowns and the table.
        
        :return: None.
        :rtype: None
        """
        self.register_student_box["values"] = [
            f"{s.student_id} - {s.name}" for s in self.students]
        self.assign_instructor_box["values"] = [
            f"{i.instructor_id} - {i.name}" for i in self.instructors]
        course_values = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.register_course_box["values"] = course_values
        self.assign_course_box["values"] = course_values
        self.refresh_table()

    def refresh_table(self):
        """Fill the Treeview, applying the current search filter.
        
        :return: None.
        :rtype: None
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        query = self.search_entry.get().strip().lower()

        for student in self.students:
            courses = ", ".join(c.course_id for c in student.registered_courses)
            if self.matches(query, student.name, student.student_id, courses):
                self.tree.insert("", "end", values=("Student", student.student_id,
                                                    student.name, student.age,
                                                    student.get_email(), courses))

        for instructor in self.instructors:
            courses = ", ".join(c.course_id for c in instructor.assigned_courses)
            if self.matches(query, instructor.name, instructor.instructor_id,
                            courses):
                self.tree.insert("", "end",
                                 values=("Instructor", instructor.instructor_id,
                                         instructor.name, instructor.age,
                                         instructor.get_email(), courses))

        for course in self.courses:
            instructor_name = course.instructor.name if course.instructor else "-"
            if self.matches(query, course.course_name, course.course_id,
                            course.course_id):
                self.tree.insert("", "end", values=("Course", course.course_id,
                                                    course.course_name, "", "",
                                                    instructor_name))

    @staticmethod
    def matches(query, name, record_id, courses):
        """Check whether a record contains the search text.
        
        :param query: Lowercase search text; an empty string matches all records.
        :type query: str
        :param name: Student, instructor or course name.
        :type name: str
        :param record_id: Record ID.
        :type record_id: str
        :param courses: Course text to search.
        :type courses: str
        :return: True if the query occurs in any searched field, otherwise False.
        :rtype: bool
        """
        if not query:
            return True
        return (query in name.lower() or query in record_id.lower()
                or query in courses.lower())

    # ------------------------------------------------------------------
    # Edit and delete
    # ------------------------------------------------------------------

    def selected_record(self):
        """Read the type and ID of the selected table row.
        
        Display an information dialog if no row is selected.
        
        :return: Record type and ID, or (None, None) if nothing is selected.
        :rtype: tuple
        """
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("No selection", "Select a record first")
            return None, None
        values = self.tree.item(selection[0], "values")
        return values[0], values[1]

    def delete_selected(self):
        """Ask for confirmation and delete the selected record.
        
        Remove its registration or assignment links and refresh the interface.
        
        :return: None.
        :rtype: None
        """
        record_type, record_id = self.selected_record()
        if not record_type:
            return
        if not messagebox.askyesno("Confirm",
                                   f"Delete {record_type} {record_id}?"):
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
        """Open a small window to edit the selected record.
        
        :return: None.
        :rtype: None
        """
        record_type, record_id = self.selected_record()
        if not record_type:
            return

        window = tk.Toplevel(self.root)
        window.title(f"Edit {record_type}")
        entries = {}

        if record_type == "Course":
            course = self.find_course(record_id)
            fields = [("Course Name", course.course_name)]
        else:
            person = (self.find_student(record_id) if record_type == "Student"
                      else self.find_instructor(record_id))
            fields = [("Name", person.name), ("Age", str(person.age)),
                      ("Email", person.get_email())]

        for row, (label, value) in enumerate(fields):
            tk.Label(window, text=label).grid(row=row, column=0, sticky="e",
                                              padx=5, pady=2)
            entry = tk.Entry(window, width=30)
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=5, pady=2)
            entries[label] = entry

        def save_changes():
            try:
                if record_type == "Course":
                    course.course_name = validate_non_empty(
                        entries["Course Name"].get(), "Course name")
                else:
                    person.name = validate_non_empty(entries["Name"].get(), "Name")
                    person.age = validate_age(entries["Age"].get())
                    person.set_email(entries["Email"].get())
            except ValueError as error:
                messagebox.showerror("Invalid input", str(error), parent=window)
                return
            window.destroy()
            self.refresh_all()

        tk.Button(window, text="Save", command=save_changes).grid(
            row=len(fields), column=0, columnspan=2, pady=8, sticky="ew")

    # ------------------------------------------------------------------
    # Save and load
    # ------------------------------------------------------------------

    def save_to_file(self):
        """Save all records to a JSON file chosen in the file dialog.
        
        Cancel without saving if no filename is selected.
        
        :raises OSError: If the selected file cannot be written.
        
        :return: None.
        :rtype: None
        """
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if not filename:
            return
        save_data(filename, self.students, self.instructors, self.courses)
        messagebox.showinfo("Saved", "Data saved to " + filename)

    def load_from_file(self):
        """Load records from a JSON file chosen in the file dialog.
        
        Cancel if no file is selected. Display an error dialog for file access,
        invalid JSON or missing data keys; refresh the interface after a successful load.
        
        :return: None.
        :rtype: None
        """
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filename:
            return
        try:
            self.students, self.instructors, self.courses = load_data(filename)
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror("Load failed", str(error))
            return
        self.refresh_all()
        messagebox.showinfo("Loaded", "Data loaded from " + filename)


if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementApp(root)
    root.mainloop()
