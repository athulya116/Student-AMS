from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import  login as auth_login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import get_user_model
from core.models import StudentProfile, FacultyProfile

User = get_user_model()


# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm-password')
#         role = request.POST.get('role')

#         # Validate required fields (as before)...

#         if password != confirm_password:
#             messages.error(request, 'Passwords do not match.')
#             return render(request, 'Student_AMS/signup.html')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already taken.')
#             return render(request, 'Student_AMS/signup.html')

#         # Create User
#         user = User.objects.create_user(username=username, password=password)

#         if role == 'student':
#             email = request.POST.get('student-email')
#             phone = request.POST.get('student-phone')
#             department = request.POST.get('student-department')
#             # roll_no = request.POST.get('rollno')

#             # Save email to User model
#             user.email = email
#             user.save()

#             # Create Student profile
#             StudentProfile.objects.create(
#                 user=user,
#                 # roll_no=roll_no,
#                 phone=phone,
#                 department=department,
#             )

#         elif role == 'faculty':
#             email = request.POST.get('faculty-email')
#             phone = request.POST.get('faculty-phone')
#             department = request.POST.get('faculty-department')
#             # faculty_id = request.POST.get('faculty-id')

#             user.email = email
#             user.save()

#             # Create Faculty profile
#             FacultyProfile.objects.create(
#                 user=user,
#                 # faculty_id=faculty_id,
#                 phone=phone,
#                 department=department,
#             )

#         messages.success(request, 'Account created successfully! Please login.')
#         return redirect('login')

#     return render(request, 'Student_AMS/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check role and redirect
            if role == 'student' and hasattr(user, 'role'):
                auth_login(request, user)
                return redirect('studentHome')
            elif role == 'faculty' and hasattr(user, 'role'):
                auth_login(request, user)
                return redirect('facultyHome')
            elif role == 'admin' and user.is_superuser:
                auth_login(request, user)
                return redirect('adminHome')
            else:
                messages.error(request, "User role mismatch.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'Student_AMS/login.html')


def home(request):
    return render(request, 'Student_AMS/index.html')

def about(request):
    return render(request, 'Student_AMS/about.html')

def contact(request):
    return render(request, 'Student_AMS/contact.html')

def department(request):
    return render(request, 'Student_AMS/departments.html')

# def tologin(request):
#     return render(request, 'Student_AMS/login.html')

def toSignup(request):
    return render(request, 'Student_AMS/signup.html')

def forgotPassword(request):
    return render(request, 'Student_AMS/forgotPassword.html')

def custom_404_view(request, exception):
    return render(request, 'Student_AMS/404.html', status=404)
