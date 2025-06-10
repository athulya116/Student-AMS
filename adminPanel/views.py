import calendar
from collections import defaultdict
from datetime import date, datetime
from django.utils import timezone
import json
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from core.models import Attendance, StudentProfile, User, FacultyProfile
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from core.models import Department



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
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if Department.objects.filter(name__iexact=name).exists():
            messages.error(request, "Department with this name already exists.")
        else:
            Department.objects.create(name=name, description=description)
            messages.success(request, "Department added successfully.")
            return redirect('adminDepartment')

    return render(request, 'Student_AMS/addDepartment.html')

@never_cache
@admin_required
def adminDepartment(request):
    departments = Department.objects.all()
    return render(request, 'Student_AMS/adminDepartments.html', {'departments': departments})

@never_cache
@admin_required
def adminStudentAttendanceView(request):
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


    return render(request, "Student_AMS/attendanceRecords.html", {
        "attendance_json": json.dumps(attendance_by_month)
    })

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
            return render(request,'Student_AMS/adminAddFaculty.html',{
                'faculty_id_exists':True,
                'form':request.POST
            })
            # messages.error(request, 'Faculty ID or Email already exists.')
        except Exception as e:
            return render(request,'Student_AMS/adminAddFaculty.html',{
                'error':str(e),
                'form':request.POST
            })
            # messages.error(request, f'Error: {str(e)}')

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
@csrf_protect
def adminEditStudentAttendance(request):

    if request.method == "GET":
        admn_no = request.GET.get("admn_no")
        if not admn_no:
            messages.error(request, "Admission number is required.")
            return redirect('studentAttendance')

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

        return render(request, 'Student_AMS/adminEditStudentAttendance.html', context)
    
        

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
