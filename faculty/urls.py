from django.urls import path
from . import views

urlpatterns = [
    path('facultyHome/',views.facultyHome, name='facultyHome'),
    path('studentList/',views.studentList, name='studentList'),
    path('facultyStudentAttendanceView/',views.facultyStudentAttendanceView, name='facultyStudentAttendanceView'),
    path('facultyEditProfile/',views.facultyEditProfile, name='facultyEditProfile'),
    path('facultyStudentProfileEdit/<str:admn_no>/',views.facultyStudentProfileEdit, name='facultyStudentProfileEdit'),
    path('facultyStudentProfileDelete/<str:admn_no>/',views.facultyDeleteStudent, name='facultyDeleteStudent'),
    path('facultyEditStudentAttendance/',views.facultyEditStudentAttendance, name='facultyEditStudentAttendance'),
    path('facultyAddStudent/', views.facultyAddStudent, name='facultyAddStudent'),
]
