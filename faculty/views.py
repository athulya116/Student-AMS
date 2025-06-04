from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from core.models import StudentProfile, User, FacultyProfile
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import update_session_auth_hash  # ✅ At the top with other imports



def faculty_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'role') and request.user.role == 'faculty':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to view this page.")
    return wrapper


@never_cache
@faculty_required
def facultyHome(request):
    user = request.user
    try:
        faculty_profile = FacultyProfile.objects.get(user=user)
    except FacultyProfile.DoesNotExist:
        faculty_profile = None

    # Example stats (can replace with real data later)
    total_students = 120
    todays_attendance_percent = 75

    context = {
        'user': user,
        'faculty_profile': faculty_profile,
        'total_students': total_students,
        'todays_attendance_percent': todays_attendance_percent,
    }
    return render(request, 'Student_AMS/facultyHome.html', context)


@never_cache
@faculty_required
def facultyAddStudent(request):
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
                return redirect('facultyAddStudent')

        except IntegrityError:
            messages.error(request, 'Admission number or Roll number already exists.')
        except Exception as e:
            messages.error(request, f'Error occurred: {str(e)}')

    return render(request, 'Student_AMS/facultyAddStudent.html')

@never_cache
@faculty_required
def studentList(request):
    students = StudentProfile.objects.select_related('user').all()
    return render(request, 'Student_AMS/studentList.html', {'students': students})

@never_cache
@faculty_required
def facultyStudentAttendanceView(request):
    return render(request, 'Student_AMS/studentAttendanceFacultyView.html')

@never_cache
@faculty_required
def facultyEditProfile(request):
    user = request.user

    try:
        faculty_profile = FacultyProfile.objects.get(user=user)
    except FacultyProfile.DoesNotExist:
        messages.error(request, "Faculty profile not found.")
        return redirect('facultyHome')

    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # 🔁 Update User model
        user.full_name = full_name
        user.email = email
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # 🔐 prevent logout after password change
        user.save()

        # 🔁 Update FacultyProfile model
        faculty_profile.phone = phone
        faculty_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('facultyHome')

    # For GET request – autofill the form
    context = {
        'form': {
            'fullName': user.full_name,
            'email': user.email,
            'phone': faculty_profile.phone,
            'facultyId': faculty_profile.faculty_id,
            'department': faculty_profile.department
        }
    }

    return render(request, 'Student_AMS/facultyEditProfile.html', context)

@never_cache
@faculty_required
def facultyStudentProfileEdit(request, admn_no):
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
        return redirect('studentList')

    context = {
        'student': student,
        'user': student.user,
    }
    return render(request, 'Student_AMS/facultyStudentProfileEdit.html', context)

@never_cache
@faculty_required
def facultyEditStudentAttendance(request):
    return render(request, 'Student_AMS/editStudentAttendance.html')

# def tofacultyAddStudent(request):
#     return render(request, 'Student_AMS/facultyAddStudent.html')

@never_cache
@faculty_required
def facultyDeleteStudent(request, admn_no):
    if request.method == 'POST':
        student = get_object_or_404(StudentProfile, admn_no=admn_no)

        # Delete linked user (this will also delete the profile due to on_delete=CASCADE)
        student.user.delete()
        messages.success(request, "Student deleted successfully.")
        
    return redirect('studentList')  # Adjust this to your actual student list view name