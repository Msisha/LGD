from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TrainingRequestViewSet, CourseViewSet, ProgressViewSet, FeedbackViewSet,
    dashboard_overview, course_progress_analytics
)

router = DefaultRouter()
router.register('training_requests', TrainingRequestViewSet, basename='training_requests')
router.register('courses', CourseViewSet, basename='courses')
router.register('progress', ProgressViewSet, basename='progress')
router.register('feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_overview, name='dashboard_overview'),
    path('analytics/progress/', course_progress_analytics, name='course_progress_analytics'),
]
