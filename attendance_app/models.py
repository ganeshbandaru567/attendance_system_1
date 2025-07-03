from django.db import models
from datetime import date

SECTION_CHOICES = [
    ('ECE-A', 'ECE-A'),
    ('ECE-B', 'ECE-B'),
    ('ECE-C', 'ECE-C'),
    ('ECE-D', 'ECE-D'),
]

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    is_present = models.BooleanField(default=False)


class StudentLogin(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Student)
def create_student_login(sender, instance, created, **kwargs):
    if created:
        StudentLogin.objects.create(
            student=instance,
            username=instance.roll_number,  # You said: username = name
            password=instance.name  # You said: password = roll_number
        )
