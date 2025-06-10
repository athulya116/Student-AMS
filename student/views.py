from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from core.models import StudentProfile
from django.contrib.auth import update_session_auth_hash  # ✅ At the top with other imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from core.models import Attendance, StudentProfile
from django.shortcuts import render
from django.utils import timezone
from core.models import Attendance
from datetime import date, timedelta
from collections import defaultdict
import calendar
import json
from datetime import datetime


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
    student = request.user.studentprofile
    attendance_qs = Attendance.objects.filter(student=student)

    # Create dict for quick lookup: {date: status}
    attendance_dict = {att.date: att.status for att in attendance_qs}

    today = timezone.localdate()
    all_data = defaultdict(list)

    # Month name mapping (lowercase keys for JS usage)
    month_name = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }

    # Loop through months up to current month
    for month in range(1, today.month + 1):
        days_in_month = calendar.monthrange(today.year, month)[1]
        
        for day in range(1, days_in_month + 1):
            current_date = date(today.year, month, day)
            if current_date > today:
                continue  # skip future dates
            
            weekday_name = calendar.day_name[current_date.weekday()]  # Monday, Tuesday, etc.
        
            weekday = weekday_name  # e.g. 'Monday'
        
            # your existing code to determine status
            if current_date.weekday() >= 5:
                status = "Holiday"
            elif current_date in attendance_dict:
                status = attendance_dict[current_date]
            else:
                status = "Absent"
        
            all_data[month_name[month]].append({
                "date": current_date.strftime("%Y-%m-%d"),
                "weekday": weekday,
                "status": status
            })

       
    available_months = list(all_data.keys())

    return render(request, "Student_AMS/studentShowAttendance.html", {
        "attendance_json": json.dumps(all_data),
        "available_months": available_months,
    })

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
        return redirect('studentEditProfile')

    # For GET request – prefill form
    return render(request, 'Student_AMS/studentEditProfile.html', {
        'student_profile': student_profile,
        'user': user
    })



@never_cache
@student_required
def markAttendance(request):
    if request.method == 'POST':
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('markAttendance')

        att_date = request.POST.get('date')
        status = request.POST.get('status')

        try:
            att_date_obj = datetime.strptime(att_date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            return redirect('markAttendance')

        if att_date_obj != date.today():
            messages.error(request, "You can only mark attendance for today.")
            return redirect('markAttendance')

        # if Attendance.objects.filter(student=student_profile, date=att_date_obj).exists():
        #     messages.warning(request, "You have already marked attendance for today.")
        # else:
        #     Attendance.objects.create(student=student_profile, date=att_date_obj, status=status)
        #     messages.success(request, "Attendance marked successfully.")
        
        today_record = Attendance.objects.filter(student=student_profile, date=att_date_obj).first()

        if today_record:
            if today_record.status != 'Absent':  # or use: if today_record.status in ['Present', 'On Leave']
                messages.warning(request, "You have already marked attendance for today.")
            else:
                today_record.status = status
                today_record.save()
                messages.success(request, "Attendance marked successfully.")
        else:
            Attendance.objects.create(student=student_profile, date=att_date_obj, status=status)
            messages.success(request, "Attendance marked successfully.")

        return redirect('markAttendance')

    return render(request, 'Student_AMS/markattendance.html', {
        'today_date': date.today().isoformat()
    })

# def markAttendance(request):
#     if request.method == 'POST':
#         today = date.today()
#         att_date_obj = datetime.strptime(att_date, "%Y-%m-%d").date()
#         try:
#             student_profile = StudentProfile.objects.get(user=request.user)
#         except StudentProfile.DoesNotExist:
#             messages.error(request, "Student profile not found.")
#             return redirect('markAttendance')

#         att_date = request.POST.get('date')
#         status = request.POST.get('status')

#         # if att_date != date.today().isoformat():
#         #     messages.error(request, "You can only mark attendance for today.")
#         #     return redirect('markAttendance')

#         # # if Attendance.objects.filter(student=student_profile, date=att_date).exists():
#         # #     messages.warning(request, "You have already marked attendance for today.")
#         # if Attendance.objects.filter(student=student_profile, date=att_date_obj).exists():
#         #     messages.warning(request, "You have already marked attendance for today.")
#         # else:
#         #     Attendance.objects.create(student=student_profile, date=att_date, status=status)
#         #     messages.success(request, "Attendance marked successfully.")
        
#         try:
#             att_date_obj = datetime.strptime(att_date, "%Y-%m-%d").date()
#         except ValueError:
#             messages.error(request, "Invalid date format.")
#             return redirect('markAttendance')

#         if att_date_obj != date.today():
#             messages.error(request, "You can only mark attendance for today.")
#             return redirect('markAttendance')

#         if Attendance.objects.filter(student=student_profile, date=att_date_obj).exists():
#             messages.warning(request, "You have already marked attendance for today.")


#         return redirect('markAttendance')

#     return render(request, 'Student_AMS/markattendance.html', {
#         'today_date': date.today().isoformat()
#     })
@never_cache
def logout_view(request):
    logout(request)  # clears session and logs out user
    return redirect('login')  # or wherever you want to redirect