from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from core.models import StudentProfile, User, FacultyProfile
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden,JsonResponse
from django.contrib.auth import update_session_auth_hash  
from collections import defaultdict
import json
import calendar
from datetime import date,datetime
from django.utils import timezone
from core.models import StudentProfile, Attendance
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET,require_POST
from django.db.models.functions import TruncMonth
from calendar import monthrange



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
    students = StudentProfile.objects.all()
    today = timezone.localdate()
    month_name = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }

    attendance_by_month = defaultdict(list)

    for student in students:
        attendance_qs = Attendance.objects.filter(student=student)
        attendance_dict = {att.date: att.status for att in attendance_qs}
        print(student)
        
        for month in range(1, today.month + 1):
            days_in_month = calendar.monthrange(today.year, month)[1]
            present = 0
            absent = 0
            holyday = 0

            for day in range(1, days_in_month + 1):
                current_date = date(today.year, month, day)
                if current_date > today:
                    continue

                weekday = current_date.weekday()
                if weekday >= 5:
                    holyday += 1
                elif current_date in attendance_dict:
                    if attendance_dict[current_date] == 'Present':
                        present += 1
                    else:
                        absent += 1
                else:
                    absent += 1

            total = present + absent + holyday
            percentage = (present / (present + absent)) * 100 if (present + absent) > 0 else 0

            attendance_by_month[month_name[month]].append({
                "name": student.full_name,
                "admn_no": student.admn_no,
                "dept": student.department,
                "present": present,
                "absent": absent,
                "holyday": holyday,
                "total": total,
                "percentage": round(percentage, 2)
            })
            # print(f"Student ID: {student.admn_no}, Name: '{student.user.get_full_name()}'")


    return render(request, "Student_AMS/studentAttendanceFacultyView.html", {
        "attendance_json": json.dumps(attendance_by_month)
    })


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
        return redirect('facultyStudentProfileEdit')

    context = {
        'student': student,
        'user': student.user,
    }
    return render(request, 'Student_AMS/facultyStudentProfileEdit.html', context)

@never_cache
@faculty_required
@csrf_protect
def facultyEditStudentAttendance(request):
    if request.method == "GET":
        admn_no = request.GET.get("admn_no")
        if not admn_no:
            messages.error(request, "Admission number is required.")
            return redirect('facultyStudentAttendanceView')

        student = get_object_or_404(StudentProfile, admn_no=admn_no)

        
        # New code: Always show Jan to current month
        current_date = datetime.now()
        month_choices = []
        for m in range(1, current_date.month + 1):  # January to current month
            dt = datetime(current_date.year, m, 1)
            month_choices.append(dt.strftime("%B %Y"))
        
        selected_month = request.GET.get('month')
        if selected_month:
            try:
                selected_dt = datetime.strptime(selected_month, "%B %Y")
            except ValueError:
                selected_dt = datetime(current_date.year, current_date.month, 1)
        else:
            selected_dt = datetime(current_date.year, current_date.month, 1)


        attendance_records = Attendance.objects.filter(
            student=student,
            date__year=selected_dt.year,
            date__month=selected_dt.month
        ).order_by('date')

        days_in_month = (datetime(selected_dt.year + (selected_dt.month // 12), ((selected_dt.month % 12) + 1), 1) -
                         datetime(selected_dt.year, selected_dt.month, 1)).days

        attendance_status_list = ['Absent'] * days_in_month
        
        for day in range(1, days_in_month + 1):
            date_obj = datetime(selected_dt.year, selected_dt.month, day)
            weekday = date_obj.weekday()

            if weekday in (5, 6):  # Saturday or Sunday
                attendance_status_list[day - 1] = 'Holiday'
            else:
                record = next((r for r in attendance_records if r.date.day == day), None)
                if record:
                    attendance_status_list[day - 1] = record.status
                else:
                    attendance_status_list[day - 1] = 'Absent'


        # month_choices = [m.strftime("%B %Y") for m in months]

        context = {
            'student': student,
            'month_choices': month_choices,
            'selected_month': selected_dt.strftime("%B %Y"),
            'attendance_status_list': attendance_status_list,
            'days_in_month': range(1, days_in_month + 1),
        }
        # print("Months found:", months)

        return render(request, 'Student_AMS/editStudentAttendance.html', context)
    
        

    elif request.method == "POST":
        admn_no = request.POST.get('admn_no')
        month_str = request.POST.get('month')
        statuses = request.POST.getlist('status')  # multiple status values

        if not (admn_no and month_str and statuses):
            messages.error(request, "Missing required data.")
            return redirect(request.path + f"?admn_no={admn_no}&month={month_str}")

        student = get_object_or_404(StudentProfile, admn_no=admn_no)

        try:
            selected_dt = datetime.strptime(month_str, "%B %Y")
        except ValueError:
            messages.error(request, "Invalid month format.")
            return redirect(request.path + f"?admn_no={admn_no}&month={month_str}")

        today = datetime.now()
        days_in_month = (datetime(selected_dt.year + (selected_dt.month // 12), ((selected_dt.month % 12) + 1), 1) -
                         datetime(selected_dt.year, selected_dt.month, 1)).days

        for day, status in enumerate(statuses, start=1):
            if day > days_in_month:
                break

            # Skip future days in current month
            if selected_dt.year == today.year and selected_dt.month == today.month and day > today.day:
                continue

            date_for_record = datetime(selected_dt.year, selected_dt.month, day)

            Attendance.objects.update_or_create(
                student=student,
                date=date_for_record,
                defaults={'status': status}
            )

        messages.success(request, "Attendance updated successfully.")
        return redirect(request.path + f"?admn_no={admn_no}&month={month_str}")

    else:
        return HttpResponse(status=405)


@never_cache
@faculty_required
def facultyDeleteStudent(request, admn_no):
    if request.method == 'POST':
        student = get_object_or_404(StudentProfile, admn_no=admn_no)

        # Delete linked user (this will also delete the profile due to on_delete=CASCADE)
        student.user.delete()
        messages.success(request, "Student deleted successfully.")
        
    return redirect('studentList')  # Adjust this to your actual student list view name