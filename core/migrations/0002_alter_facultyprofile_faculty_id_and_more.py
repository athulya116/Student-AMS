# Generated by Django 5.2.1 on 2025-06-04 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultyprofile',
            name='faculty_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='roll_no',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
