from django.db import models
from django.contrib.auth.models import AbstractUser
class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.subject}"

SECURITY_QUESTIONS = [
    ("What is your pet's name?", "What is your pet's name?"),
    ("What is your mother's maiden name?", "What is your mother's maiden name?"),
    ("What was your first school?", "What was your first school?"),
    ("What is your favorite food?", "What is your favorite food?"),
]

class CustomUser(AbstractUser):
    security_question = models.CharField(max_length=255, choices=SECURITY_QUESTIONS, blank=True)
    security_answer = models.CharField(max_length=255, blank=True)