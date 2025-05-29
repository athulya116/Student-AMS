from django.shortcuts import render

# Create your views here.

def facultyHome(request):
    return render(request, 'Student_AMS/facultyHome.html')

def studentList(request):
    return render(request, 'Student_AMS/studentList.html')

def facultyStudentAttendanceView(request):
    return render(request, 'Student_AMS/studentAttendanceFacultyView.html')

def facultyEditProfile(request):
    return render(request, 'Student_AMS/facultyEditProfile.html')

def facultyStudentProfileEdit(request):
    return render(request, 'Student_AMS/facultyStudentProfileEdit.html')

def facultyEditStudentAttendance(request):
    return render(request, 'Student_AMS/editStudentAttendance.html')