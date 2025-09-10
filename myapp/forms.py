from django import forms
import re
from .models import Student ,Teacher
from .models import Registration , CourseContent

MAJOR_CHOICES = [
    ("ریاضی", "ریاضی"),
    ("آمار" , "آمار"),
    ("کامپیوتر","کامپیوتر"),
]

from django import forms
import re
from .models import Student, Teacher

MAJOR_CHOICES = [
    ("ریاضی", "ریاضی"),
    ("آمار", "آمار"),
    ("کامپیوتر", "کامپیوتر"),
]

SUBJECT_CHOICES = [
    ("دروس تخصصی", "تخصصی"),
    ("دروس عمومی", "عمومی"),
]

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    major = forms.ChoiceField(choices=MAJOR_CHOICES, widget=forms.RadioSelect)
    student_id = forms.CharField()  
    class Meta:
        model = Student
        fields = ["username", "password", "first_name", "last_name", "student_id", "date_of_birth", "major"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Student.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return username

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"]
        if Student.objects.filter(_student_id=student_id).exists():  
            raise forms.ValidationError("این کد ملی قبلاً ثبت شده است.")
        return student_id

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        pattern = r'^\d{4}/\d{2}/\d{2}$'
        if not re.match(pattern, dob):
            raise forms.ValidationError("تاریخ باید به فرمت YYYY/MM/DD وارد شود.")
        return dob

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("رمز عبور باید حداقل یک حرف بزرگ داشته باشد.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("رمز عبور باید حداقل یک حرف کوچک داشته باشد.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.student_id = self.cleaned_data["student_id"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class TeacherRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, widget=forms.RadioSelect)
    teacher_id = forms.CharField()  

    class Meta:
        model = Teacher
        fields = ["username", "password", "first_name", "last_name", "teacher_id", "date_of_birth", "subject"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Teacher.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return username

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data["teacher_id"]
        if Teacher.objects.filter(_teacher_id=teacher_id).exists():  
            raise forms.ValidationError("این کد ملی قبلاً ثبت شده است.")
        return teacher_id

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        pattern = r"^\d{4}/\d{2}/\d{2}$"
        if not re.match(pattern, dob):
            raise forms.ValidationError("تاریخ باید به فرمت YYYY/MM/DD وارد شود.")
        return dob

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("رمز عبور باید حداقل یک حرف بزرگ داشته باشد.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("رمز عبور باید حداقل یک حرف کوچک داشته باشد.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.teacher_id = self.cleaned_data["teacher_id"]  
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20 ,widget=forms.PasswordInput())

class GradeForm(forms.ModelForm):
    grade = forms.DecimalField(max_digits=4,decimal_places=2,widget=forms.NumberInput(attrs={"step": "0.01", "min": 0, "max": 20}),)
    class Meta:
        model = Registration
        fields = [] 
        widgets = {"grade": forms.NumberInput(attrs={"step": "0.01", "min": 0, "max": 20}), }

    def save(self, commit=True):
        registration = super().save(commit=False)
        registration.grade = self.cleaned_data["grade"]
        if commit:
            registration.save()
        return registration

class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = ["course", "title", "file"]
