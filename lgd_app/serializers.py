from rest_framework import serializers
from .models import User, TrainingRequest, Course, Progress, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TrainingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingRequest
        fields = ['id', 'title', 'description', 'status', 'requested_by']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'assigned_to', 'status']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'course', 'employee', 'completion_percentage']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'course', 'employee', 'comments', 'rating']
