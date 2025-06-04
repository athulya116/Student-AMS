from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from core.models import StudentProfile
from django.contrib.auth import update_session_auth_hash  # ✅ At the top with other imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



def student_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'role') and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to view this page.")
    return wrapper


# def studentHome(request):
#     user = request.user  # The logged-in user

#     # If you have extra profile info in a related model, fetch it here
#     # For example, if you have a StudentProfile linked to User:
#     # student_profile = StudentProfile.objects.get(user=user)

#     context = {
#         'user': user,
#         # 'student_profile': student_profile,  # optional
#     }
#     return render(request, 'Student_AMS/studentHome.html', context)


@never_cache
@student_required
def studentHome(request):
    user = request.user
    try:
        student_profile = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        student_profile = None  # or handle error

    context = {
        'user': user,
        'student_profile': student_profile,
    }
    return render(request, 'Student_AMS/studentHome.html', context)


# def studentHome(request):
#     return render(request, 'Student_AMS/studentHome.html')


@never_cache
@student_required
def studentShowAttendance(request):
    return render(request, 'Student_AMS/studentShowAttendance.html')

# def studentEditProfile(request):
#     return render(request, 'Student_AMS/studentEditProfile.html')

@never_cache
@student_required
def studentEditProfile(request):
    user = request.user
    try:
        student_profile = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('studentHome')

    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Update StudentProfile
        student_profile.full_name = full_name
        student_profile.phone = phone
        student_profile.save()

        # Update User model
        user.email = email
        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  # ✅ Keep logged in
        else:
            user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('studentHome')

    # For GET request – prefill form
    return render(request, 'Student_AMS/studentEditProfile.html', {
        'student_profile': student_profile,
        'user': user
    })


@never_cache
@student_required
def markAttendance(request):
    return render(request, 'Student_AMS/markAttendance.html')

@never_cache
def logout_view(request):
    logout(request)  # clears session and logs out user
    return redirect('login')  # or wherever you want to redirect