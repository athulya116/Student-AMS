from django.core.management.base import BaseCommand
from core.models import StudentProfile, Attendance
from datetime import date

class Command(BaseCommand):
    help = 'Mark absent for students who did not mark attendance today'

    def handle(self, *args, **kwargs):
        today = date.today()
        students = StudentProfile.objects.all()

        for student in students:
            already_marked = Attendance.objects.filter(student=student, date=today).exists()

            if not already_marked:
                Attendance.objects.create(student=student, date=today, status='Absent')
                self.stdout.write(self.style.WARNING(f"{student.admn_no} marked as Absent"))
            else:
                self.stdout.write(self.style.SUCCESS(f"{student.admn_no} already marked"))
