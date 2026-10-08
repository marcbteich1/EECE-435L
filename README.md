# EECE 435L

Marc Bteich — Solo Lab 4

This is the School Management System from Labs 2 and 3. It manages students, instructors, courses, course registration, and instructor assignments. The Tkinter and PyQt5 interfaces use the same classes in `part1_oop.py` and can load and save the same JSON files.

## Setup

Install Python 3.12 with Tkinter support. Tkinter is included in the standard Windows Python installer.

From the repository folder, run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run Tkinter

From the repository folder:

```powershell
cd Lab3_Marc_Bteich
..\.venv\Scripts\python.exe part2_tkinter.py
```

## Run PyQt5

From the `Lab3_Marc_Bteich` folder:

```powershell
..\.venv\Scripts\python.exe part3_pyqt.py
```

## Using the interfaces

Both interfaces open with an empty table. Click **Load Data** and select `435Ldb.json` to load the sample records.

- Fill in the forms to add students, instructors, and courses.
- Choose a student and a course, then click **Register Course**.
- Choose an instructor and a course, then click **Assign Course**.
- Search by name, ID, or course. In Tkinter, click **Search** or **Clear**. In PyQt5, the table updates as you type.
- Select a row and click **Edit Selected** or **Delete Selected**.
- Click **Save Data** before closing to keep your records. PyQt5 also has **Export to CSV**.

To use records from one interface in the other, save them as JSON, then open that file with **Load Data** in the other interface. Registrations and instructor assignments are kept. Reload the file after making changes in the other window.
