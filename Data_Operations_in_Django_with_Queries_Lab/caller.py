import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries
from main_app.models import Student


# Task 1
def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )

    student2 = Student(student_id='FE0054',
                       first_name='Jane',
                       last_name='Smith',
                       email='jane.smith@university.com')
    student2.save()

    student3 = Student(student_id='FH2014',
                       first_name='Alice',
                       last_name='Johnson',
                       birth_date='1998-02-10',
                       email='alice.johnson@university.com')
    student3.save()

    student4 = Student(student_id='FH2015',
                       first_name='Bob',
                       last_name='Wilson',
                       birth_date='1996-11-25',
                       email='bob.wilson@university.com')
    student4.save()


# add_students()
# print(Student.objects.all())

# Task 2
def get_students_info():
    all_students = Student.objects.all()
    result = []
    for student in all_students:
        result.append(
            f"Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}")
    return "\n".join(result)


#
# print(get_students_info())

# Task 3
def update_students_emails():
    students = Student.objects.all()
    for student in students:
        new_email = student.email.replace('university.com', 'uni-students.com')
        student.email = new_email
        student.save()


#
# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

# Task 4
def truncate_students():
    all_students = Student.objects.all()
    all_students.delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
