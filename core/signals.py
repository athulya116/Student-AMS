from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, FacultyProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            # Avoid duplicate creation if somehow called twice
            if not StudentProfile.objects.filter(user=instance).exists():
                # Use username as admn_no or adjust as per your logic
                StudentProfile.objects.create(user=instance, admn_no=instance.username)
        elif instance.role == 'faculty':
            if not FacultyProfile.objects.filter(user=instance).exists():
                FacultyProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'student':
        # Use getattr to avoid exceptions if profile doesn't exist (rare)
        student_profile = getattr(instance, 'studentprofile', None)
        if student_profile:
            student_profile.save()
    elif instance.role == 'faculty':
        faculty_profile = getattr(instance, 'facultyprofile', None)
        if faculty_profile:
            faculty_profile.save()
