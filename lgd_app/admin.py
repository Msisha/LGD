from django.contrib import admin
from .models import User, TrainingRequest, Course, Progress, Feedback

admin.site.register(User)
admin.site.register(TrainingRequest)
admin.site.register(Course)
admin.site.register(Progress)
admin.site.register(Feedback)
