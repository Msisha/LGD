from django.core.mail import send_mail
from django_cron import CronJobBase, Schedule
from django.utils.timezone import now
from .models import Course

class NotificationSystem:
    @staticmethod
    def send_course_assignment_notification(employee, course):
        subject = f"New Course Assigned: {course.title}"
        message = (
            f"Dear {employee.username},\n\nYou have been assigned a new course: {course.title}. "
            "Please log in to the system to view details."
        )
        send_mail(subject, message, 'no-reply@lddg.com', [employee.email])

    @staticmethod
    def send_deadline_reminder(employee, course):
        subject = f"Reminder: Complete Your Course - {course.title}"
        message = (
            f"Dear {employee.username},\n\nThis is a reminder to complete the course: {course.title}. "
            "The deadline is approaching soon."
        )
        send_mail(subject, message, 'no-reply@lgd.com', [employee.email])

class NotificationCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Runs every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'lgd.notification_cron'

    def do(self):
        courses = Course.objects.filter(status='in_progress')
        for course in courses:
            employee = course.assigned_to
            if (course.deadline - now()).days <= 3:
                NotificationSystem.send_deadline_reminder(employee, course)
