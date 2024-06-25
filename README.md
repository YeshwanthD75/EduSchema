# EduSchema
Application for Managing Courses, Students and  Instructors in an online learning platform.

# Education Management System

This project is a comprehensive education management system implemented using Python, MySQL, and Tkinter. The system provides functionality to manage instructors, courses, students, enrollments, and assessments within an educational institution. It includes features for adding, deleting, searching, and sorting records, along with a backup mechanism for deleted data.

## Features

1. **Database Management:**
   - Connection to a MySQL database.
   - Creation and usage of the 'education' database.
   - Creation of tables for instructors, courses, students, enrollments, and assessments.
   - Backup tables for storing deleted records.

2. **CRUD Operations:**
   - Add, delete, and view records for instructors, courses, students, enrollments, and assessments.
   - Search for instructors by name.
   - Sort instructors by name in ascending or descending order.

3. **Graphical User Interface (GUI):**
   - A Tkinter-based GUI with tabs for managing different entities (instructors, courses, students, enrollments, assessments).
   - Forms for adding and deleting records.
   - Views for displaying search and sorted results.
   - Backup functionality accessible through the GUI.

## Installation and Setup

1. **Install Dependencies:**
   - Python 3.x
   - MySQL server
   - Tkinter library (usually included with Python)

2. **Configure MySQL Connection:**
   - Ensure MySQL server is running.
   - Update the `create_connection()` function with your MySQL server credentials:
     ```python
     connection = mysql.connector.connect(
         host='localhost',
         user='root',
         password='your_password',  # Replace with your MySQL password
         database='education'       # Assuming 'education' database already exists
     )
     ```

3. **Run the Application:**
   - Execute the script:
     ```sh
     python education_management_system.py
     ```

## Usage

1. **Instructors Management:**
   - Add a new instructor by filling in the name, email, phone, and bio fields, then clicking "Add Instructor."
   - Delete an instructor by providing the instructor's name and clicking "Delete Instructor."
   - Search for instructors by name using the search field and "Search" button.
   - Sort instructors by name using the "Sort Ascending" and "Sort Descending" buttons.
   - View all instructors and back up instructor data using the respective buttons.

2. **Courses Management:**
   - Similar functionality as instructors management for adding, deleting, viewing, and backing up courses.

3. **Students Management:**
   - Similar functionality as instructors management for adding, deleting, viewing, and backing up students.

4. **Enrollments Management:**
   - Add and delete enrollments using student and course IDs.
   - View all enrollments and back up enrollment data.

5. **Assessments Management:**
   - Add and delete assessments.
   - View all assessments and back up assessment data.
