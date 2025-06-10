from django.urls import path
from . import views

urlpatterns = [
    path('adminHome/',views.adminHome, name='adminHome'),
    path('addDepartment/',views.addDepartment, name='addDepartment'),
    path('adminDepartment/',views.adminDepartment, name='adminDepartment'),
    path('studentAttendance/',views.adminStudentAttendanceView, name='studentAttendance'),
    path('studentProfile/',views.studentProfile, name='studentProfile'),
    path('manageStudent/',views.manageStudent, name='manageStudent'),
    path('manageFaculty/',views.manageFaculty, name='manageFaculty'),
    path('adminProfile/',views.adminProfile, name='adminProfile'),
    path('adminAddStudent/',views.adminAddStudent, name='adminAddStudent'),
    path('adminAddFaculty/',views.adminAddFaculty, name='adminAddFaculty'),
    path('adminStudentProfileEdit/<str:admn_no>/',views.adminEditStudent, name='adminStudentProfileEdit'),
    path('adminStudentProfileDelete/<str:admn_no>/',views.adminDeleteStudent, name='adminDeleteStudent'),

    path('adminEditFaculty/<str:faculty_id>/',views.adminEditFaculty, name='adminEditFaculty'),
    path('adminDeleteFaculty/<str:faculty_id>/',views.adminDeleteFaculty, name='adminDeleteFaculty'),

    path('adminEditStudentAttendance/',views.adminEditStudentAttendance, name='adminEditStudentAttendance'),
]
