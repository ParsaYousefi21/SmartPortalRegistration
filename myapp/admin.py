from django.contrib import admin
from .models import Teacher, Student 
from .models import Course , Registration , CourseContent

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=("username","first_name", "last_name", "_student_id", "date_of_birth", "major")
    search_fields = ("first_name", "last_name", "_student_id")
    list_filter = ("major",)
    ordering = ("last_name",)
    fieldsets = (
    ("اطلاعات شخصی", {"fields": ("first_name", "last_name", "date_of_birth")}),
    ("اطلاعات تحصیلی", {"fields": ("_student_id", "major")}),)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("username","first_name", "last_name","_teacher_id","date_of_birth","subject")
    search_fields = ("first_name", "last_name", "_teacher_id", "username")
    list_filter = ("subject",)
    ordering = ("last_name",)
    fieldsets = (
    ("اطلاعات شخصی", {'fields': ("first_name","last_name","_teacher_id","date_of_birth")}), 
    ("اطلاعات شغلی", {'fields': ["subject"]}),)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "course_type", "major","day1", "start_time1", "end_time1","day2", "start_time2", "end_time2","capacity", "unit")
    filter_horizontal = ["needs"]
    list_filter = ("course_type",)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("student_name","course","_grade","finalized_status","registered_date")

    def student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    student_name.admin_order_field = "student__last_name"  
    student_name.short_description = "نام و نام خانوادگی"

    def finalized_status(self, obj):
        return "✅ نهایی شده" if obj.is_finalized else "❌ نهایی نشده"
    finalized_status.short_description = "وضعیت انتخاب واحد"

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ("course", "teacher", "title", "file")  
