from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TrainingRequest, Course, Progress, Feedback
from .serializers import (
    UserSerializer, TrainingRequestSerializer, CourseSerializer,
    ProgressSerializer, FeedbackSerializer
)
from .permissions import IsAdmin, IsAccountManager, IsEmployee
from django.db.models import Avg, Count

class TrainingRequestViewSet(ModelViewSet):
    queryset = TrainingRequest.objects.all()
    serializer_class = TrainingRequestSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsAccountManager()]
        elif self.action in ['approve_request', 'reject_request']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['POST'])
    def approve_request(self, request, pk=None):
        training_request = self.get_object()
        training_request.status = 'approved'
        training_request.save()
        return Response({'status': 'Request approved'})

    @action(detail=True, methods=['POST'])
    def reject_request(self, request, pk=None):
        training_request = self.get_object()
        training_request.status = 'rejected'
        training_request.save()
        return Response({'status': 'Request rejected'})

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'assign_course']:
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['POST'])
    def assign_course(self, request, pk=None):
        course = self.get_object()
        employee_id = request.data.get('employee_id')
        try:
            employee = User.objects.get(id=employee_id, role='employee')
            course.assigned_to = employee
            course.save()
            return Response({'status': f'Course assigned to {employee.username}'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid employee ID'}, status=400)

class ProgressViewSet(ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['POST'])
    def update_progress(self, request, pk=None):
        progress = self.get_object()
        completion_percentage = request.data.get('completion_percentage')
        if completion_percentage is not None:
            progress.completion_percentage = completion_percentage
            progress.save()
            return Response({'status': 'Progress updated'})
        return Response({'error': 'Invalid completion percentage'}, status=400)

class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.action in ['list']:
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['create']:
            return [IsAuthenticated(), IsEmployee()]
        return [IsAuthenticated()]

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def dashboard_overview(request):
    total_requests = TrainingRequest.objects.count()
    approved_requests = TrainingRequest.objects.filter(status='approved').count()
    rejected_requests = TrainingRequest.objects.filter(status='rejected').count()
    pending_requests = TrainingRequest.objects.filter(status='pending').count()

    total_courses = Course.objects.count()
    completed_courses = Course.objects.filter(status='completed').count()

    average_feedback_rating = Feedback.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    data = {
        'total_requests': total_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'pending_requests': pending_requests,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'average_feedback_rating': average_feedback_rating,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def course_progress_analytics(request):
    total_courses = Course.objects.count()
    completed_courses = Course.objects.filter(status='completed').count()
    overall_completion_rate = (completed_courses / total_courses) * 100 if total_courses else 0

    progress_data = Progress.objects.values('course__title').annotate(
        average_completion=Avg('completion_percentage'),
        total_employees=Count('employee'),
    )

    response_data = {
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'overall_completion_rate': overall_completion_rate,
        'course_details': list(progress_data),
    }
    return Response(response_data)
