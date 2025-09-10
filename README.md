# 🎓 Smart Portal Registration

A Smart Portal Registration in django for managing students, teachers, courses, registrations, grading, and course content.  
It provides **role-based dashboards**, authentication, course selection with conflict detection, GPA calculation, grading, and data export to JSON.
The project is built using **Object-Oriented Programming (OOP)** principles to keep the code modular, extendable, and easy to maintain.
The entire application is in **Persian (Farsi)**, and the UI uses the **Vazirmatn font** for better readability and a modern look.

## Table of Contents
- [Features](#)
- [Design & Architecture](#)
- [Tech Stack](#)
- [Project Structure](#)
- [Requirements](#)
- [Installation & Setup](#)
- [Contributing](#)
- [License](#)

## ✨ Features

### 👨‍🎓 Students registration and login
- Register with personal details, username ,first_name , last_name , student_id , date_of_birth , password and major.
- Login with username and password

### Student dashboard Features
- Browse and select courses (with **capacity limits** & **schedule conflict detection**).  
- Simulated **checkout system** for finalizing course selection.  
- View **term reports** with GPA, passed units, and failed units.  
- Access **course contents** (PDFs, images, videos, etc.).  

### 👨‍🏫 Teachers register and login
- Register with personal details, username ,first_name , last_name , student_id , date_of_birth , password and major.
- Login with username and password

### Teacher dashboard Features
- View their courses and enrolled students.  
- Assign grades to students.  
- Upload and manage **course contents** (files, resources, materials).  

### ⚙️ Admin Panel
- Manage **Students, Teachers, Courses, Registrations, and Course Content**.  
- Search, filter, and order records easily.  
- Custom display fields for clarity (student names, finalized status, etc.).  

### 📤 Data Export
- Export all students to **`exports/students.json`**.  
- Export all teachers to **`exports/teachers.json`**.

-  **Why do we use JSON export?**  
  - Portable and lightweight format  
  - Easy to share with other applications and systems  
  - Human-readable and editable  
  - Works well for backup and data migration

## 🧩 Design & Architecture

This project is designed using **OOP concepts**:

- **Classes** represent core entities such as `Student`, `Teacher`, `Course`, `Registration`, and `CourseContent`  
- **Inheritance**: both students and teachers extend from the base `User` class  
- **Encapsulation**: validation and data handling are defined inside models and forms  
- **Polymorphism**: methods like `get_role()` behave differently depending on the user type  
- **Modularity**: code is organized into separate files like `models`, `views`, `forms`, and `utils`

## 🛠️ Tech Stack

- **Backend**: Django (Python)  
- **Frontend**: Django Templates + Bootstrap + Vazirmatn font  
- **Database**: SQLite (default, can be switched to PostgreSQL/MySQL)  
- **Auth**: Django built-in authentication system  
- **Export**: JSON file output (students & teachers)  
- **Language**: Persian (Farsi)

### 📂 Project Structure
myapp/

**│── admin.py**      # Admin panel configuration

**│── forms.py**          # Forms and validation

**│── models.py**         # Database models (Student, Teacher, Course, etc.)

**│── utils.py**          # Helper functions (JSON export)

**│── views.py**          # Application logic

**│── templates/**        # HTML templates

**│── static/**           # CSS, JS, and Vazirmatn font

**exports/**              # JSON output files

## 🛠️ Requirements
asgiref==3.9.1

Django==5.2.4

sqlparse==0.5.3

tzdata==2025.2

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ParsaYousefi21/SmartPortalRegistration
   cd SmartPortalRegistration
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Start the server**:
   ```bash
   python manage.py runserver
   ```
Now you can open the project in your browser at:
http://127.0.0.1:8000/

### 🤝 Contributing
We welcome contributions to improve this project. Please follow these steps:

1. **Fork** the repository (create your own copy of the project).
2. **Create a new branch** (git checkout -b feature/YourFeature).
3. **Commit your changes** (git commit -m 'add features').
4. **Push your branch** (git push origin feature/YourFeature).
5. **Open a Pull Request**.

All contributions will be reviewed, and constructive feedback may be provided to ensure quality.

## License
None
