from django.shortcuts import render , redirect , get_object_or_404
from django.http import JsonResponse
from .forms import StudentRegistrationForm , TeacherRegistrationForm 
from .forms import LoginForm , GradeForm , CourseContentForm 
from .models import Course , Student , Teacher , Registration , CourseContent 
from django.contrib.auth import login , authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from myapp.utils import export_students_to_json , export_teachers_to_json 
from django.db.models import Q

def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            export_students_to_json()
            return render(request , "registration_success.html")
        else:
            return render(request, "register_student.html", {"form": form})
    else:
        form = StudentRegistrationForm()
    return render(request , "register_student.html" , {"form": form})

def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            export_teachers_to_json()
            return render(request , "registration_success.html")
        else:
            return render(request, "register_teacher.html", {"form": form})
    else:
        form = TeacherRegistrationForm()
    return render(request , "register_teacher.html" , {"form": form})
 
def role_selection(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role == "student":
            return redirect("register_student")
        elif role == "teacher":
            return redirect("register_teacher")
        
    return render(request , "role_selection.html")

def login_users(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if hasattr(user, "student"):
                    return redirect("student_dashboard")
                elif hasattr(user, "teacher"):
                    return redirect("teacher_dashboard")
                else:
                    messages.error(request, "⛔ نوع کاربر مشخص نیست.")
            else:
                messages.error(request, "⛔ نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

@login_required
def student_dashboard(request):
    if not hasattr(request.user, "student"):
        messages.error(request, "⛔ دسترسی غیرمجاز.")
        return redirect("login")

    student = get_object_or_404(Student, id=request.user.id)
    courses = student.courses.all().prefetch_related("needs")
    registrations = Registration.objects.filter(student=student).select_related("student", "course")

    context = {
        "courses": courses,
        "registrations": registrations,
    }
    return render(request, "student_dashboard.html", context)

@login_required
def checkout(request):
    student = Student.objects.get(user_ptr_id=request.user.id)
    regs = Registration.objects.filter(student=student, is_finalized=False)

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        status = request.POST.get("payment_status")
        if status == "success":
            regs.update(is_finalized=True)
            return JsonResponse({"status": "success", "message": "✅ پرداخت موفق و انتخاب واحد نهایی شد."})
        elif status == "fail":
            return JsonResponse({"status": "fail", "message": "⛔ پرداخت ناموفق بود. لطفاً دوباره تلاش کنید."})
    
    return render(request, "checkout.html", {"registrations": regs})

@login_required
def choose_course(request):
    student = Student.objects.get(user_ptr_id=request.user.id)

    courses = Course.objects.filter(
        Q(course_type="public") |
        Q(course_type="shared") |
        Q(course_type="exclusive", major=student.major)
    ).distinct()

    regs = Registration.objects.filter(student=student)
    selected_ids = regs.values_list("course_id", flat=True)
    finalized = regs.filter(is_finalized=True).exists()

    if request.method == "POST" and not finalized:
        course_id = request.POST.get("course_id")
        cancel_id = request.POST.get("cancel_course_id")

        if course_id:
            new_course = get_object_or_404(Course, id=course_id)
            current_count = Registration.objects.filter(course=new_course).count()

            if current_count >= new_course.capacity:
                messages.error(request, "⛔ ظرفیت این درس تکمیل شده است.")
            else:
                for reg in regs:
                    existing_course = reg.course
                    if existing_course.day1 == new_course.day1:
                        if existing_course.start_time1 < new_course.end_time1 and new_course.start_time1 < existing_course.end_time1:
                            messages.error(request, f"⛔ این درس با درس دیگری در روز {new_course.get_day1_display()} تداخل دارد.")
                            break
                    if new_course.day2:
                        if existing_course.day1 == new_course.day2:
                            if existing_course.start_time1 < new_course.end_time2 and new_course.start_time2 < existing_course.end_time1:
                                messages.error(request, f"⛔ این درس با درس دیگری در روز {new_course.get_day2_display()} تداخل دارد.")
                                break
                        if existing_course.day2:
                            if existing_course.day2 == new_course.day2:
                                if existing_course.start_time2 < new_course.end_time2 and new_course.start_time2 < existing_course.end_time2:
                                    messages.error(request, f"⛔ این درس با درس دیگری در روز {new_course.get_day2_display()} تداخل دارد.")
                                    break
                else:
                    Registration.objects.create(student=student, course=new_course)

        if cancel_id:
            Registration.objects.filter(student=student, course_id=cancel_id, is_finalized=False).delete()

        if request.POST.get("checkout") == "1":
            return redirect("checkout")

        regs = Registration.objects.filter(student=student)
        selected_ids = regs.values_list("course_id", flat=True)

    course_capacity_left = {
        course.id: course.capacity - Registration.objects.filter(course=course).count()
        for course in courses}

    context = {
        "student": student,
        "courses": courses,
        "registrations": regs,
        "selected_courses_ids": selected_ids,
        "finalized": finalized,
        "course_capacity_left": course_capacity_left,
    }

    return render(request, "choose_course.html", context)


@login_required
def term_report(request):
    student = get_object_or_404(Student, pk=request.user.id)

    registrations = Registration.objects.filter(student=student).select_related("course__teacher")

    total_score = 0
    total_units = 0
    passed_units = 0
    failed_units = 0

    for reg in registrations:
        if reg.grade is not None:
            total_score += reg.grade
            total_units += reg.course.unit
            if reg.grade >= 10:
                passed_units += reg.course.unit
            else:
                failed_units += reg.course.unit

    gpa = total_score / total_units if total_units > 0 else 0

    context = {
        "registrations": registrations,
        "gpa": round(gpa, 2),
        "passed_units": passed_units,
        "failed_units": failed_units,
    }

    return render(request, "term_report.html", context)

@login_required
def course_contents(request):
    student = get_object_or_404(Student, id=request.user.id)
    registrations = Registration.objects.filter(student=student).select_related("course")

    course_ids = [reg.course.id for reg in registrations]
    contents = CourseContent.objects.filter(course__id__in=course_ids).select_related("course")

    for content in contents:
        file_name = content.file.name.lower()
        if file_name.endswith(".pdf"):
            content.file_type = "pdf"
        elif file_name.endswith((".png", ".jpg", ".jpeg", ".webp")):
            content.file_type = "image"
        elif content.file.url.lower().endswith(".mp4"):
            content.file_type = "video"
        else:
            content.file_type = "other"

    return render(request, "course_contents.html", {"contents": contents})

@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, "teacher"):
        messages.error(request, "⛔ دسترسی غیرمجاز.")
        return redirect("login")

    teacher = get_object_or_404(Teacher, id=request.user.id)
    courses = Course.objects.filter(teacher=teacher)
    regs = Registration.objects.filter(course__in=courses).select_related("student", "course")

    context = {
        "courses": courses,
        "registrations": regs,
    }
    return render(request, "teacher_dashboard.html", context)

@login_required
def add_grade(request):
    student_id = request.GET.get("student")
    course_id = request.GET.get("course")

    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    registration = get_object_or_404(Registration, student=student, course=course)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            return redirect("teacher_dashboard")
    else:
        form = GradeForm(instance=registration)

    return render(request, "add_grade.html", {"form": form,"registration": registration,})

@login_required
def add_content(request):
    if request.method == "POST":
        form = CourseContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.teacher = Teacher.objects.get(id=request.user.id)
            content.save()
            return redirect("add_content")
    else:
        form = CourseContentForm()

    contents = CourseContent.objects.filter(teacher__id=request.user.id).order_by("-id")

    return render(request, "add_content.html", {
        "form": form,
        "contents": contents
    })

@login_required
def delete_content(request, pk):
    content = get_object_or_404(CourseContent, pk=pk, teacher=request.user)
    if request.method == "POST":
        content.delete()
        return redirect("add_content")





