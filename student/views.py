from django.shortcuts import render

# Create your views here.

def studentHome(request):
    return render(request, 'Student_AMS/studentHome.html')

def studentShowAttendance(request):
    return render(request, 'Student_AMS/studentShowAttendance.html')

def studentEditProfile(request):
    return render(request, 'Student_AMS/studentEditProfile.html')

def markAttendance(request):
    return render(request, 'Student_AMS/markAttendance.html')