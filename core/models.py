from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    # Define user roles
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admn_no = models.CharField(max_length=20, primary_key=True, unique=True)
    # admn_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=150, null=True, blank=True)

    roll_no = models.CharField(max_length=50, unique=True, blank=True,null=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Student: {self.user.username}"

class FacultyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=50, unique=True, blank=True,null=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Faculty: {self.user.username}"