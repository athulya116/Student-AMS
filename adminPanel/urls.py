from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.adminHome, name='adminHome'),
    path('addDepartment/',views.addDepartment, name='addDepartment'),
    path('adminDepartment/',views.adminDepartment, name='adminDepartment'),
    path('studentAttendance/',views.studentAttendance, name='studentAttendance'),
    path('studentProfile/',views.studentProfile, name='studentProfile'),
    path('manageStudent/',views.manageStudent, name='manageStudent'),
    path('manageFaculty/',views.manageFaculty, name='manageFaculty'),
    path('adminProfile/',views.adminProfile, name='adminProfile'),
    path('adminAddStudent/',views.adminAddStudent, name='adminAddStudent'),
    path('adminAddFaculty/',views.adminAddFaculty, name='adminAddFaculty'),
    path('adminEditStudent/',views.adminEditStudent, name='adminEditStudent'),
    path('adminEditFaculty/',views.adminEditFaculty, name='adminEditFaculty'),
    path('adminEditStudentAttendance/',views.adminEditStudentAttendance, name='adminEditStudentAttendance'),
]
