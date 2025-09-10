from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, verbose_name="نام کاربری")
    first_name = models.CharField(max_length=20, verbose_name="نام")
    last_name = models.CharField(max_length=20, verbose_name="نام خانوادگی")
    date_of_birth = models.CharField(max_length=10, verbose_name="تاریخ تولد")

    def get_role(self):
        raise NotImplementedError("Subclasses must implement get_role()")

MAJOR_CHOICES = [
    ("ریاضی", "ریاضی"),
    ("آمار", "آمار"),
    ("کامپیوتر", "کامپیوتر"),
]

class Student(User):
    _student_id = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")  
    courses = models.ManyToManyField("Course", blank=True, verbose_name="دروس")
    major = models.CharField(choices=MAJOR_CHOICES, verbose_name="رشته")

    class Meta:
        verbose_name = "دانش آموز"
        verbose_name_plural = "دانش‌آموزان"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, new_id):
        if not new_id.isdigit():
            raise ValueError("کد ملی باید عددی باشد")
        self._student_id = new_id  

    def get_role(self):
        return "Student"


SUBJECT_CHOICES = [
    ("دروس تخصصی", "تخصصی"),
    ("دروس عمومی", "عمومی"),
]


class Teacher(User):
    _teacher_id = models.CharField(max_length=10, unique=True, verbose_name="کد ملی") 
    subject = models.CharField(choices=SUBJECT_CHOICES, verbose_name="عنوان")

    class Meta:
        verbose_name = "معلم"
        verbose_name_plural = "معلمان"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def teacher_id(self):
        return self._teacher_id  

    @teacher_id.setter
    def teacher_id(self, new_id):
        if not new_id.isdigit():
            raise ValueError("کد ملی باید عددی باشد")
        self._teacher_id = new_id  

    def get_role(self):
        return "Teacher"

CLASS_TYPE_CHOICES = [
    ("public", "عمومی"),
    ("shared", "مشترک بین رشته‌ها"),
    ("exclusive", "تخصصی"),
]

MAJOR_CHOICES = [
    ("ریاضی", "ریاضی"),
    ("آمار", "آمار"),
    ("کامپیوتر", "کامپیوتر"),
]

class Course(models.Model):
    DAYS = [
        ('sat', 'شنبه'),
        ('sun', 'یکشنبه'),
        ('mon', 'دوشنبه'),
        ('tue', 'سه‌شنبه'),
        ('wed', 'چهارشنبه'),
        ('thu', 'پنج‌شنبه'),
        ('fri', 'جمعه'),
    ]
    title = models.CharField(max_length=100, verbose_name="عنوان")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="معلم")
    course_type = models.CharField(choices=CLASS_TYPE_CHOICES , verbose_name="نوع درس")
    major = models.CharField(choices=MAJOR_CHOICES, blank=True, verbose_name="رشته")
    needs = models.ManyToManyField("self", blank=True, symmetrical=False, verbose_name="پیش‌ نیازها")
    capacity = models.PositiveIntegerField(verbose_name="ظرفیت")
    unit = models.PositiveSmallIntegerField(verbose_name="تعداد واحد")
    day1 = models.CharField(max_length=10, choices=DAYS, verbose_name="روز اول")
    start_time1 = models.TimeField(verbose_name="ساعت شروع")
    end_time1 = models.TimeField(verbose_name="ساعت پایان")
    day2 = models.CharField(choices=DAYS, blank=True, null=True, verbose_name="روز دوم")
    start_time2 = models.TimeField(blank=True, null=True, verbose_name="ساعت شروع")
    end_time2 = models.TimeField(blank=True, null=True, verbose_name="ساعت پایان")

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"

    def __str__(self):
        return f"{self.title} - {self.teacher}"


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="دانش آموز")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="درس")
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت نام")
    is_finalized = models.BooleanField(default=False, verbose_name="وضعیت انتخاب واحد")
    _grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="نمره")

    class Meta:
        verbose_name = "ثبت نام"
        verbose_name_plural = "ثبت نام ها"

    def __str__(self):
        return f"{self.student} - {self.course}"

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, new_grade):
        if new_grade is not None and (new_grade < 0 or new_grade > 20):
            raise ValueError("نمره باید بین 0 و 20 باشد")
        self._grade = new_grade


class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="درس")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="معلم")
    title = models.CharField(max_length=255, verbose_name="عنوان")
    file = models.FileField(upload_to='contents/', verbose_name="فایل")

    class Meta:
        verbose_name = "محتوا"
        verbose_name_plural = "محتواها"

    def __str__(self):
        return f"{self.course} - {self.title}"
