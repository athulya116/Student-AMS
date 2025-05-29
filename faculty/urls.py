from django.urls import path
from . import views

urlpatterns = [
    path('facultyHome/',views.facultyHome, name='facultyHome'),
    path('studentList/',views.studentList, name='studentList'),
    path('facultyStudentAttendanceView/',views.facultyStudentAttendanceView, name='facultyStudentAttendanceView'),
    path('facultyEditProfile/',views.facultyEditProfile, name='facultyEditProfile'),
    path('facultyStudentProfileEdit/',views.facultyStudentProfileEdit, name='facultyStudentProfileEdit'),
    path('facultyEditStudentAttendance/',views.facultyEditStudentAttendance, name='facultyEditStudentAttendance'),
]
