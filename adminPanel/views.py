from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from core.models import StudentProfile, User, FacultyProfile
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to view this page.")
    return wrapper



@never_cache
@admin_required
def adminHome(request):
    return render(request, 'Student_AMS/adminHome.html') 

@never_cache
@admin_required
def addDepartment(request):
    return render(request, 'Student_AMS/addDepartment.html')

@never_cache
@admin_required
def adminDepartment(request):
    return render(request, 'Student_AMS/adminDepartments.html')

@never_cache
@admin_required
def studentAttendance(request):
    return render(request, 'Student_AMS/attendanceRecords.html')

@never_cache
@admin_required
def studentProfile(request):
    return render(request, 'Student_AMS/studentProfile.html')

@never_cache
@admin_required
def manageStudent(request):
    students = StudentProfile.objects.select_related('user').all()
    return render(request, 'Student_AMS/manageStudents.html', {'students': students})

@never_cache
@admin_required
def manageFaculty(request):
    faculties = FacultyProfile.objects.select_related('user').all()
    return render(request, 'Student_AMS/manageFaculty.html',{'faculties': faculties})

@never_cache
@admin_required
def adminProfile(request):
    return render(request, 'Student_AMS/adminProfile.html')


@never_cache
@admin_required
def adminAddStudent(request):
    if request.method == 'POST':
        admn_no = request.POST['admn_no']
        full_name = request.POST['fullName']
        email = request.POST['email']
        phone = request.POST['phone']
        department = request.POST['department']
        roll_no = request.POST['roll_no']
        password = request.POST['password']

        try:
            with transaction.atomic():
                # Create user with admn_no as username
                user = User.objects.create(
                    username=admn_no,
                    full_name=full_name,
                    email=email,
                    password=make_password(password),  # always hash passwords!
                    role='student',
                )

                # StudentProfile will be auto-created via signals
                profile = user.studentprofile
                profile.roll_no = roll_no
                profile.phone = phone
                profile.department = department
                profile.full_name = full_name  # optional - if you want it in profile too
                profile.save()

                messages.success(request, 'Student added successfully!')
                return redirect('adminAddStudent')

        except IntegrityError:
            messages.error(request, 'Admission number or Roll number already exists.')
        except Exception as e:
            messages.error(request, f'Error occurred: {str(e)}')

    return render(request, 'Student_AMS/adminAddStudent.html')


@never_cache
@admin_required
def adminAddFaculty(request):
    if request.method == 'POST':
        full_name = request.POST['fullName']
        email = request.POST['email']
        phone = request.POST['phone']
        department = request.POST['department']
        faculty_id = request.POST['faculty_id']
        password = request.POST['password']

        try:
            with transaction.atomic():
                # Create User (username = faculty_id)
                user = User.objects.create(
                    username=faculty_id,
                    full_name=full_name,
                    email=email,
                    password=make_password(password),
                    role='faculty',
                )

                # FacultyProfile auto-created via signals
                faculty_profile = user.facultyprofile
                faculty_profile.faculty_id = faculty_id
                faculty_profile.phone = phone
                faculty_profile.department = department
                faculty_profile.save()

                messages.success(request, 'Faculty added successfully!')
                return redirect('adminAddFaculty')

        except IntegrityError:
            messages.error(request, 'Faculty ID or Email already exists.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'Student_AMS/adminAddFaculty.html')


@never_cache
@admin_required
def adminEditStudent(request, admn_no):
    student = get_object_or_404(StudentProfile, admn_no=admn_no)
    user = student.user

    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        roll_no = request.POST.get('rollNumber')
        password = request.POST.get('password')

        # Update user
        user.full_name = full_name
        user.email = email
        if password:  # only update if new password is provided
            user.password = make_password(password)
        user.save()

        # Update profile
        student.phone = phone
        student.department = department
        student.roll_no = roll_no
        student.full_name = full_name  # optional
        student.save()

        messages.success(request, "Student profile updated successfully.")
        return redirect('manageStudent')

    context = {
        'student': student,
        'user': student.user,
    }
    return render(request, 'Student_AMS/adminEditStudent.html', context)



@never_cache
@admin_required
def adminEditFaculty(request, faculty_id):
    faculty_profile = get_object_or_404(FacultyProfile, faculty_id=faculty_id)
    user = faculty_profile.user

    if request.method == 'POST':
        user.full_name = request.POST.get('fullName')
        user.email = request.POST.get('email')
        faculty_profile.phone = request.POST.get('phone')
        faculty_profile.department = request.POST.get('department')

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()
        faculty_profile.save()

        messages.success(request, "Faculty profile updated successfully.")
        return redirect('manageFaculty')  # Change to your actual list view

    context = {
        'facultyId': faculty_profile.faculty_id,
        'full_name': user.full_name,
        'email': user.email,
        'phone': faculty_profile.phone,
        'department': faculty_profile.department,
    }
    return render(request, 'Student_AMS/adminEditFaculty.html', context)


@never_cache
@admin_required
def adminEditStudentAttendance(request):
    return render(request, 'Student_AMS/adminEditStudentAttendance.html')


@never_cache
@admin_required
def adminDeleteStudent(request, admn_no):
    if request.method == 'POST':
        student = get_object_or_404(StudentProfile, admn_no=admn_no)
        student.user.delete()  # Automatically deletes StudentProfile due to on_delete=models.CASCADE

        # Optional: add success message
        messages.success(request, "Student deleted successfully.")

    return redirect('manageStudent')  # Replace with your actual student list view name

@never_cache
@admin_required
def adminDeleteFaculty(request, faculty_id):
    if request.method == 'POST':
        faculty = get_object_or_404(FacultyProfile, faculty_id=faculty_id)
        faculty.user.delete()  # Automatically deletes FacultyProfile due to on_delete=models.CASCADE   
        # Optional: add success message
        messages.success(request, "Faculty deleted successfully.")
    return redirect('manageFaculty')
