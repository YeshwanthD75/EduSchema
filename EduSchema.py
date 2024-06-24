import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Global list to store deleted items for backup purposes
deleted_items = []

# Database connection configuration
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yesh2004',  # Replace with your MySQL password
            database='education'  # Assuming 'education' database already exists
        )
        if connection.is_connected():
            print("Connection to MySQL server successful")
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Function to create and use the education database
def create_use_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS education")
        cursor.execute("USE education")
        print("Database 'education' created and selected successfully.")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")

# Function to create tables in the education database
def create_tables(connection):
    queries = [
        """CREATE TABLE IF NOT EXISTS `instructors` (
                `instructor_id` INTEGER PRIMARY KEY AUTO_INCREMENT, 
                `instructor_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255),
                `bio` TEXT
            )""",
        """CREATE TABLE IF NOT EXISTS `course` (
                `course_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_name` VARCHAR(255) NOT NULL,
                `description` TEXT,
                `credit_hours` INTEGER,
                `instructor_id` INTEGER,
                FOREIGN KEY (`instructor_id`) REFERENCES `instructors` (`instructor_id`) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS `students` (
                `student_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `student_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255)
            )""",
        """CREATE TABLE IF NOT EXISTS `enrolments` (
                `enrolment_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_id` INTEGER,
                `student_id` INTEGER,
                `enrolment_date` DATE,
                `completion_status` ENUM('enrolled', 'completed'),
                FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE,
                FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS `assessments` (
                `assessment_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_id` INTEGER,
                `assessment_name` VARCHAR(255) NOT NULL,
                `max_score` INTEGER,
                `given_by` INTEGER,
                `given_to` INTEGER,
                FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE,
                FOREIGN KEY (`given_by`) REFERENCES `instructors` (`instructor_id`) ON DELETE CASCADE,
                FOREIGN KEY (`given_to`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_instructors` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `instructor_id` INTEGER,
                `instructor_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255),
                `bio` TEXT,
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_course` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_id` INTEGER,
                `course_name` VARCHAR(255) NOT NULL,
                `description` TEXT,
                `credit_hours` INTEGER,
                `instructor_id` INTEGER,
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_students` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `student_id` INTEGER,
                `student_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255),
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_assessments` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `assessment_id` INTEGER,
                `course_id` INTEGER,
                `assessment_name` VARCHAR(255) NOT NULL,
                `max_score` INTEGER,
                `given_by` INTEGER,
                `given_to` INTEGER,
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )"""
    ]
    try:
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()
        print("Tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")

# Function to insert a new instructor into the database
def insert_instructor(connection, instructor_name, email, phone, bio):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO instructors (instructor_name, email, phone, bio) VALUES (%s, %s, %s, %s)"
        values = (instructor_name, email, phone, bio)
        cursor.execute(query, values)
        connection.commit()
        print("Instructor inserted successfully.")
        messagebox.showinfo("Success", "Instructor inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting instructor: {err}")
        messagebox.showerror("Error", f"Error inserting instructor: {err}")

# Function to insert a new course into the database
def insert_course(connection, course_name, description, credit_hours, instructor_id):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO course (course_name, description, credit_hours, instructor_id) VALUES (%s, %s, %s, %s)"
        values = (course_name, description, credit_hours, instructor_id)
        cursor.execute(query, values)
        connection.commit()
        print("Course inserted successfully.")
        messagebox.showinfo("Success", "Course inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting course: {err}")
        messagebox.showerror("Error", f"Error inserting course: {err}")

# Function to insert a new student into the database
def insert_student(connection, student_name, email, phone):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO students (student_name, email, phone) VALUES (%s, %s, %s)"
        values = (student_name, email, phone)
        cursor.execute(query, values)
        connection.commit()
        print("Student inserted successfully.")
        messagebox.showinfo("Success", "Student inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting student: {err}")
        messagebox.showerror("Error", f"Error inserting student: {err}")

# Function to insert a new enrollment into the database
def insert_enrollment(connection, course_id, student_id, enrolment_date, completion_status):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO enrolments (course_id, student_id, enrolment_date, completion_status) VALUES (%s, %s, %s, %s)"
        values = (course_id, student_id, enrolment_date, completion_status)
        cursor.execute(query, values)
        connection.commit()
        print("Enrollment inserted successfully.")
        messagebox.showinfo("Success", "Enrollment inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting enrollment: {err}")
        messagebox.showerror("Error", f"Error inserting enrollment: {err}")

# Function to insert a new assessment into the database
def insert_assessment(connection, course_id, assessment_name, max_score, given_by, given_to):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO assessments (course_id, assessment_name, max_score, given_by, given_to) VALUES (%s, %s, %s, %s, %s)"
        values = (course_id, assessment_name, max_score, given_by, given_to)
        cursor.execute(query, values)
        connection.commit()
        print("Assessment inserted successfully.")
        messagebox.showinfo("Success", "Assessment inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting assessment: {err}")
        messagebox.showerror("Error", f"Error inserting assessment: {err}")

# Function to delete an instructor from the database
def delete_instructor(connection, instructor_id):
    cursor = connection.cursor()
    try:
        # Retrieve instructor details before deleting
        cursor.execute("SELECT * FROM instructors WHERE instructor_id = %s", (instructor_id,))
        instructor_data = cursor.fetchone()
        
        if instructor_data:
            # Insert into backup table
            query = "INSERT INTO backup_instructors (instructor_id, instructor_name, email, phone, bio) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, instructor_data)
        
        # Delete instructor from main table
        cursor.execute("DELETE FROM instructors WHERE instructor_id = %s", (instructor_id,))
        connection.commit()
        
        print(f"Instructor with ID {instructor_id} deleted successfully.")
        messagebox.showinfo("Success", f"Instructor with ID {instructor_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting instructor: {err}")
        messagebox.showerror("Error", f"Error deleting instructor: {err}")

# Function to delete a course from the database
def delete_course(connection, course_id):
    cursor = connection.cursor()
    try:
        # Retrieve course details before deleting
        cursor.execute("SELECT * FROM course WHERE course_id = %s", (course_id,))
        course_data = cursor.fetchone()
        
        if course_data:
            # Insert into backup table
            query = "INSERT INTO backup_course (course_id, course_name, description, credit_hours, instructor_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, course_data)
        
        # Delete course from main table
        cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
        connection.commit()
        
        print(f"Course with ID {course_id} deleted successfully.")
        messagebox.showinfo("Success", f"Course with ID {course_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting course: {err}")
        messagebox.showerror("Error", f"Error deleting course: {err}")

# Function to delete a student from the database
def delete_student(connection, student_id):
    cursor = connection.cursor()
    try:
        # Retrieve student details before deleting
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student_data = cursor.fetchone()
        
        if student_data:
            # Insert into backup table
            query = "INSERT INTO backup_students (student_id, student_name, email, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, student_data)
        
        # Delete student from main table
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        connection.commit()
        
        print(f"Student with ID {student_id} deleted successfully.")
        messagebox.showinfo("Success", f"Student with ID {student_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting student: {err}")
        messagebox.showerror("Error", f"Error deleting student: {err}")

# Function to delete an assessment from the database
def delete_assessment(connection, assessment_id):
    cursor = connection.cursor()
    try:
        # Retrieve assessment details before deleting
        cursor.execute("SELECT * FROM assessments WHERE assessment_id = %s", (assessment_id,))
        assessment_data = cursor.fetchone()
        
        if assessment_data:
            # Insert into backup table
            query = "INSERT INTO backup_assessments (assessment_id, course_id, assessment_name, max_score, given_by, given_to) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, assessment_data)
        
        # Delete assessment from main table
        cursor.execute("DELETE FROM assessments WHERE assessment_id = %s", (assessment_id,))
        connection.commit()
        
        print(f"Assessment with ID {assessment_id} deleted successfully.")
        messagebox.showinfo("Success", f"Assessment with ID {assessment_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting assessment: {err}")
        messagebox.showerror("Error", f"Error deleting assessment: {err}")

# Function to search instructors by name
def search_instructors_by_name(connection, name):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM instructors WHERE instructor_name LIKE %s"
        cursor.execute(query, (f'%{name}%',))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error searching for instructors: {err}")
        return []

# Function to sort instructors by name
def sort_instructors_by_name(connection, order='ASC'):
    cursor = connection.cursor()
    try:
        query = f"SELECT * FROM instructors ORDER BY instructor_name {order}"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error sorting instructors: {err}")
        return []

# Function to display search results
def display_search_results(connection, name):
    results = search_instructors_by_name(connection, name)
    result_window = tk.Toplevel()
    result_window.title("Search Results")

    tree = ttk.Treeview(result_window, columns=('ID', 'Name', 'Email', 'Phone', 'Bio'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Email', text='Email')
    tree.heading('Phone', text='Phone')
    tree.heading('Bio', text='Bio')
    tree.pack(fill=tk.BOTH, expand=True)

    for row in results:
        tree.insert('', tk.END, values=row)

# Function to display sorted results
def display_sorted_results(connection, order='ASC'):
    results = sort_instructors_by_name(connection, order)
    result_window = tk.Toplevel()
    result_window.title("Sorted Results")

    tree = ttk.Treeview(result_window, columns=('ID', 'Name', 'Email', 'Phone', 'Bio'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Email', text='Email')
    tree.heading('Phone', text='Phone')
    tree.heading('Bio', text='Bio')
    tree.pack(fill=tk.BOTH, expand=True)

    for row in results:
        tree.insert('', tk.END, values=row)

# Function to create the GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def create_gui(connection):
    root = tk.Tk()
    root.title("Education Management System")

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    # Create frames for each tab
    instructors_frame = ttk.Frame(notebook, width=400, height=280)
    courses_frame = ttk.Frame(notebook, width=400, height=280)
    students_frame = ttk.Frame(notebook, width=400, height=280)
    enrollments_frame = ttk.Frame(notebook, width=400, height=280)
    assessments_frame = ttk.Frame(notebook, width=400, height=280)

    instructors_frame.pack(fill='both', expand=True)
    courses_frame.pack(fill='both', expand=True)
    students_frame.pack(fill='both', expand=True)
    enrollments_frame.pack(fill='both', expand=True)
    assessments_frame.pack(fill='both', expand=True)

    # Add tabs to notebook
    notebook.add(instructors_frame, text='Instructors')
    notebook.add(courses_frame, text='Courses')
    notebook.add(students_frame, text='Students')
    notebook.add(enrollments_frame, text='Enrollments')
    notebook.add(assessments_frame, text='Assessments')

    # Helper functions
    def view_all(table_name):
        results = get_all_records(connection, table_name)
        messagebox.showinfo("All Records", f"{results}")

    def backup_data(table_name):
        backup_table_data(connection, table_name)
        messagebox.showinfo("Backup", f"Backup of {table_name} completed.")

    def delete_record(table_name, record_id):
        delete_table_record(connection, table_name, record_id)
        messagebox.showinfo("Delete", f"Record {record_id} from {table_name} deleted.")

    def sort_asc(table_name):
        display_sorted_results(connection, table_name, 'ASC')

    def sort_desc(table_name):
        display_sorted_results(connection, table_name, 'DESC')

    # Instructors tab
    ttk.Label(instructors_frame, text="Instructor Name:").grid(row=0, column=0, padx=10, pady=10)
    instructor_name_entry = ttk.Entry(instructors_frame)
    instructor_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(instructors_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
    email_entry = ttk.Entry(instructors_frame)
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(instructors_frame, text="Phone:").grid(row=2, column=0, padx=10, pady=10)
    phone_entry = ttk.Entry(instructors_frame)
    phone_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(instructors_frame, text="Bio:").grid(row=3, column=0, padx=10, pady=10)
    bio_entry = ttk.Entry(instructors_frame)
    bio_entry.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(instructors_frame, text="Instructor ID to Delete:").grid(row=4, column=0, padx=10, pady=10)
    delete_instructor_id_entry = ttk.Entry(instructors_frame)
    delete_instructor_id_entry.grid(row=4, column=1, padx=10, pady=10)

    def add_instructor():
        name = instructor_name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        bio = bio_entry.get()
        insert_instructor(connection, name, email, phone, bio)

    def delete_instructor():
        instructor_id = delete_instructor_id_entry.get()
        delete_record("instructors", instructor_id)

    ttk.Button(instructors_frame, text="Add Instructor", command=add_instructor).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(instructors_frame, text="View All Instructors", command=lambda: view_all("instructors")).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(instructors_frame, text="Backup Instructors Data", command=lambda: backup_data("instructors")).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(instructors_frame, text="Delete Instructor", command=delete_instructor).grid(row=8, column=0, columnspan=2, pady=10)
    ttk.Button(instructors_frame, text="Sort Ascending", command=lambda: sort_asc("instructors")).grid(row=9, column=0, padx=10, pady=10)
    ttk.Button(instructors_frame, text="Sort Descending", command=lambda: sort_desc("instructors")).grid(row=9, column=1, padx=10, pady=10)

    # Courses tab
    ttk.Label(courses_frame, text="Course Name:").grid(row=0, column=0, padx=10, pady=10)
    course_name_entry = ttk.Entry(courses_frame)
    course_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(courses_frame, text="Description:").grid(row=1, column=0, padx=10, pady=10)
    description_entry = ttk.Entry(courses_frame)
    description_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(courses_frame, text="Credit Hours:").grid(row=2, column=0, padx=10, pady=10)
    credit_hours_entry = ttk.Entry(courses_frame)
    credit_hours_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(courses_frame, text="Instructor ID:").grid(row=3, column=0, padx=10, pady=10)
    instructor_id_entry = ttk.Entry(courses_frame)
    instructor_id_entry.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(courses_frame, text="Course ID to Delete:").grid(row=4, column=0, padx=10, pady=10)
    delete_course_id_entry = ttk.Entry(courses_frame)
    delete_course_id_entry.grid(row=4, column=1, padx=10, pady=10)

    def add_course():
        name = course_name_entry.get()
        description = description_entry.get()
        credit_hours = credit_hours_entry.get()
        instructor_id = instructor_id_entry.get()
        insert_course(connection, name, description, credit_hours, instructor_id)

    def delete_course():
        course_id = delete_course_id_entry.get()
        delete_record("courses", course_id)

    ttk.Button(courses_frame, text="Add Course", command=add_course).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(courses_frame, text="View All Courses", command=lambda: view_all("courses")).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(courses_frame, text="Backup Courses Data", command=lambda: backup_data("courses")).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(courses_frame, text="Delete Course", command=delete_course).grid(row=8, column=0, columnspan=2, pady=10)
    ttk.Button(courses_frame, text="Sort Ascending", command=lambda: sort_asc("courses")).grid(row=9, column=0, padx=10, pady=10)
    ttk.Button(courses_frame, text="Sort Descending", command=lambda: sort_desc("courses")).grid(row=9, column=1, padx=10, pady=10)

    # Students tab
    ttk.Label(students_frame, text="Student Name:").grid(row=0, column=0, padx=10, pady=10)
    student_name_entry = ttk.Entry(students_frame)
    student_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(students_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
    student_email_entry = ttk.Entry(students_frame)
    student_email_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(students_frame, text="Phone:").grid(row=2, column=0, padx=10, pady=10)
    student_phone_entry = ttk.Entry(students_frame)
    student_phone_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(students_frame, text="Student ID to Delete:").grid(row=3, column=0, padx=10, pady=10)
    delete_student_id_entry = ttk.Entry(students_frame)
    delete_student_id_entry.grid(row=3, column=1, padx=10, pady=10)

    def add_student():
        name = student_name_entry.get()
        email = student_email_entry.get()
        phone = student_phone_entry.get()
        insert_student(connection, name, email, phone)

    def delete_student():
        student_id = delete_student_id_entry.get()
        delete_record("students", student_id)

    ttk.Button(students_frame, text="Add Student", command=add_student).grid(row=4, column=0, columnspan=2, pady=10)
    ttk.Button(students_frame, text="View All Students", command=lambda: view_all("students")).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(students_frame, text="Backup Students Data", command=lambda: backup_data("students")).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(students_frame, text="Delete Student", command=delete_student).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(students_frame, text="Sort Ascending", command=lambda: sort_asc("students")).grid(row=8, column=0, padx=10, pady=10)
    ttk.Button(students_frame, text="Sort Descending", command=lambda: sort_desc("students")).grid(row=8, column=1, padx=10, pady=10)

    # Enrollments tab
    ttk.Label(enrollments_frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
    enrollment_student_id_entry = ttk.Entry(enrollments_frame)
    enrollment_student_id_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(enrollments_frame, text="Course ID:").grid(row=1, column=0, padx=10, pady=10)
    enrollment_course_id_entry = ttk.Entry(enrollments_frame)
    enrollment_course_id_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(enrollments_frame, text="Enrollment Date:").grid(row=2, column=0, padx=10, pady=10)
    enrollment_date_entry = ttk.Entry(enrollments_frame)
    enrollment_date_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(enrollments_frame, text="Enrollment ID to Delete:").grid(row=3, column=0, padx=10, pady=10)
    delete_enrollment_id_entry = ttk.Entry(enrollments_frame)
    delete_enrollment_id_entry.grid(row=3, column=1, padx=10, pady=10)

    def add_enrollment():
        student_id = enrollment_student_id_entry.get()
        course_id = enrollment_course_id_entry.get()
        date = enrollment_date_entry.get()
        insert_enrollment(connection, student_id, course_id, date)

    def delete_enrollment():
        enrollment_id = delete_enrollment_id_entry.get()
        delete_record("enrollments", enrollment_id)

    ttk.Button(enrollments_frame, text="Add Enrollment", command=add_enrollment).grid(row=4, column=0, columnspan=2, pady=10)
    ttk.Button(enrollments_frame, text="View All Enrollments", command=lambda: view_all("enrollments")).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(enrollments_frame, text="Backup Enrollments Data", command=lambda: backup_data("enrollments")).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(enrollments_frame, text="Delete Enrollment", command=delete_enrollment).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(enrollments_frame, text="Sort Ascending", command=lambda: sort_asc("enrollments")).grid(row=8, column=0, padx=10, pady=10)
    ttk.Button(enrollments_frame, text="Sort Descending", command=lambda: sort_desc("enrollments")).grid(row=8, column=1, padx=10, pady=10)

    # Assessments tab
    ttk.Label(assessments_frame, text="Assessment Name:").grid(row=0, column=0, padx=10, pady=10)
    assessment_name_entry = ttk.Entry(assessments_frame)
    assessment_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(assessments_frame, text="Course ID:").grid(row=1, column=0, padx=10, pady=10)
    assessment_course_id_entry = ttk.Entry(assessments_frame)
    assessment_course_id_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(assessments_frame, text="Max Score:").grid(row=2, column=0, padx=10, pady=10)
    max_score_entry = ttk.Entry(assessments_frame)
    max_score_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(assessments_frame, text="Assessment ID to Delete:").grid(row=3, column=0, padx=10, pady=10)
    delete_assessment_id_entry = ttk.Entry(assessments_frame)
    delete_assessment_id_entry.grid(row=3, column=1, padx=10, pady=10)

    def add_assessment():
        name = assessment_name_entry.get()
        course_id = assessment_course_id_entry.get()
        max_score = max_score_entry.get()
        insert_assessment(connection, name, course_id, max_score)

    def delete_assessment():
        assessment_id = delete_assessment_id_entry.get()
        delete_record("assessments", assessment_id)

    ttk.Button(assessments_frame, text="Add Assessment", command=add_assessment).grid(row=4, column=0, columnspan=2, pady=10)
    ttk.Button(assessments_frame, text="View All Assessments", command=lambda: view_all("assessments")).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(assessments_frame, text="Backup Assessments Data", command=lambda: backup_data("assessments")).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(assessments_frame, text="Delete Assessment", command=delete_assessment).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(assessments_frame, text="Sort Ascending", command=lambda: sort_asc("assessments")).grid(row=8, column=0, padx=10, pady=10)
    ttk.Button(assessments_frame, text="Sort Descending", command=lambda: sort_desc("assessments")).grid(row=8, column=1, padx=10, pady=10)

    root.mainloop()

# Main program execution
def main():
    connection = create_connection()
    if connection:
        create_use_database(connection)
        create_tables(connection)
        create_gui(connection)

if __name__ == "__main__":
    main()
