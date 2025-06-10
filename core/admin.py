from django.contrib import admin
from .models import User, StudentProfile, FacultyProfile, Attendance, Department 

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(FacultyProfile)
admin.site.register(Department)

admin.site.register(Attendance)
 