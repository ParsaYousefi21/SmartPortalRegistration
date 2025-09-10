from django.urls import path
from .views import login_users , role_selection
from .views import register_student , register_teacher  
from .views import student_dashboard , teacher_dashboard , add_content , checkout
from .views import term_report , choose_course , add_grade , course_contents , delete_content

urlpatterns = [
    path('register_student/', register_student , name='register_student'),
    path('register_teacher/', register_teacher , name='register_teacher'),
    path('select-role/',role_selection, name='role_selection'),
    path('login', login_users , name='login'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path("checkout/", checkout, name="checkout"),
    path('student/choose-course/', choose_course, name='choose_course'),
    path('student/term-report/', term_report , name='term_report'),
    path('student/contents/', course_contents, name='course_contents'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('add-grade/', add_grade, name='add_grade'),
    path('teacher/add-content/', add_content, name='add_content'),
    path("delete/<int:pk>/", delete_content, name="delete_content"),
]

