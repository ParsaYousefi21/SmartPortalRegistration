import json
import os 
from .models import Student , Teacher 
from django.conf import settings

EXPORT_DIR = os.path.join(settings.BASE_DIR, "exports")

def export_students_to_json():
    students = Student.objects.all().values("username","first_name", "last_name", "_student_id", "date_of_birth","major")
    with open(os.path.join(EXPORT_DIR, "students.json"), "w" , encoding="utf-8")as f :
        json.dump(list(students), f , ensure_ascii=False, indent=2)

def export_teachers_to_json():
    teachers = Teacher.objects.all().values("username","first_name", "last_name", "_teacher_id", "date_of_birth" ,"subject")
    with open(os.path.join(EXPORT_DIR, "teachers.json"), "w" , encoding="utf-8")as f :
                json.dump(list(teachers), f , ensure_ascii=False, indent=2)



