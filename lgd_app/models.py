from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, role=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('account_manager', 'Account Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    objects = UserManager()

class TrainingRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Course(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    deadline = models.DateTimeField(null=True, blank=True)

class Progress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    completion_percentage = models.FloatField(default=100.0)

class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedback')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    comments = models.TextField()
    rating = models.IntegerField()
