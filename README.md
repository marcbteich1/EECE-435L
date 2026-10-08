# EECE 435L

School Management System by Marc Bteich, reused from Labs 2 and 3 for the solo Lab 4 Git and GitHub assignment.

The project manages students, instructors, courses, student registrations, and instructor assignments. Tkinter and PyQt5 provide alternative interfaces to the same Python classes and JSON data format. The existing SQLite implementation provides a separate database-backed PyQt5 interface.

## Project files

All original application files are in `Lab3_Marc_Bteich/`:

- `part1_oop.py`: shared classes, validation, and JSON save/load.
- `part2_tkinter.py`: Tkinter interface.
- `part3_pyqt.py`: PyQt5 interface, including CSV export.
- `part4_database.py`: SQLite operations and database-backed PyQt5 interface.
- `435Ldb.json`: fictional sample records for either JSON interface.
- `435Ldb.db`: SQLite sample database.
- `docs/`: Sphinx sources and generated HTML documentation.
- `screenshots/`: interface and database screenshots using fictional records.

## Install

Use Python 3.12 with Tcl/Tk support (included in the standard Windows Python installer). From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Tkinter, SQLite, JSON, and CSV are included with Python. PyQt5 is required for the PyQt interfaces; Sphinx and its theme are used to rebuild the existing documentation.

## Run the interfaces

From the repository root:

```powershell
cd Lab3_Marc_Bteich
..\.venv\Scripts\python.exe part2_tkinter.py
```

Close the Tkinter window when finished. To run PyQt5 from that same directory:

```powershell
..\.venv\Scripts\python.exe part3_pyqt.py
```

Both interfaces start with empty in-memory records. Click **Load Data** and select `435Ldb.json` to use the sample school records.

1. Enter a name, non-negative age, valid email, and unique ID, then click **Add Student** or **Add Instructor**. Enter a course ID and name, then click **Add Course**.
2. Select a student and course, then click **Register Course**. Select an instructor and course, then click **Assign Course**.
3. Search by name, ID, or course. Tkinter uses **Search** and **Clear**; PyQt5 filters as you type.
4. Select a table row to use **Edit Selected** or **Delete Selected**.
5. Click **Save Data** before closing to persist records as JSON. PyQt5 also supports **Export to CSV**.

To exchange data between the interfaces, save a JSON file in one interface and load that file in the other. Student enrollments and instructor assignments are preserved. Each window has its own in-memory state; changes become available to the other interface after saving and reloading.

## Existing SQLite interface

From `Lab3_Marc_Bteich/`:

```powershell
..\.venv\Scripts\python.exe part4_database.py
```

This interface automatically reads and writes `435Ldb.db` in the current working directory. It supports the same school operations plus **Backup Database** and **Restore Database**. Its SQLite files are separate from the JSON files used by Parts 2 and 3. Run it from the application directory to use the included database.

The existing `part4_database.py --demo` command resets the database records before demonstrating CRUD operations; run that demonstration only in a disposable directory if you want to preserve your records.

## Documentation

Open `Lab3_Marc_Bteich/docs/_build/html/index.html` in a browser. To rebuild from the repository root:

```powershell
.\.venv\Scripts\python.exe -m sphinx -b html Lab3_Marc_Bteich/docs Lab3_Marc_Bteich/docs/_build/html
```

## Solo Lab 4 submission

Verification performed with Python 3.12.10 and PyQt5 5.15.11: both interfaces were instantiated and their existing handlers exercised for adding records, validation, registration, instructor assignment, search, editing, deletion, and JSON exchange in both directions. PyQt5 CSV export and SQLite CRUD, search, backup/restore, and database widgets also passed. File dialogs and message boxes were controlled during these checks; this was an automated widget test, not a manual walkthrough of every desktop interaction.

The project uses `main` with meaningful commits. One student maintains both interfaces, so collaborators, feature branches, pull requests, merges, and contribution tracking are unnecessary. Tags and GitHub releases are optional.

Repository: https://github.com/marcbteich1/EECE-435L

Submit this repository link and the README on Moodle as required by the lab. The Lab 4 instruction document and local private originals are excluded from Git.
