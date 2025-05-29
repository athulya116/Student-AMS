from django.shortcuts import render

# Create your views here.

def adminHome(request):
    return render(request, 'Student_AMS/adminHome.html') 

def addDepartment(request):
    return render(request, 'Student_AMS/addDepartment.html')

def adminDepartment(request):
    return render(request, 'Student_AMS/adminDepartments.html')

def studentAttendance(request):
    return render(request, 'Student_AMS/attendanceRecords.html')

def studentProfile(request):
    return render(request, 'Student_AMS/studentProfile.html')

def manageStudent(request):
    return render(request, 'Student_AMS/manageStudents.html')

def manageFaculty(request):
    return render(request, 'Student_AMS/manageFaculty.html')

def adminProfile(request):
    return render(request, 'Student_AMS/adminProfile.html')

def adminAddStudent(request):
    return render(request, 'Student_AMS/adminAddStudent.html')

def adminAddFaculty(request):   
    return render(request, 'Student_AMS/adminAddFaculty.html')

def adminEditStudent(request):
    return render(request, 'Student_AMS/adminEditStudent.html')

def adminEditFaculty(request):   
    return render(request, 'Student_AMS/adminEditFaculty.html')

def adminEditStudentAttendance(request):
    return render(request, 'Student_AMS/adminEditStudentAttendance.html')
