from django.urls import path
from . import views

urlpatterns = [
    path('studentHome/',views.studentHome, name='studentHome'),
    path('studentShowAttendance/',views.studentShowAttendance, name='studentShowAttendance'),
    path('studentEditProfile/',views.studentEditProfile, name='studentEditProfile'),
    path('markAttendance/',views.markAttendance, name='markAttendance'),
]
