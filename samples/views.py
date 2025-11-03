from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, SampleSerializer, ReadOnlyUserSerializer, TaskSerializer
from .models import Sample, AuditLog, Task

# Create your views here.

class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class SampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows samples to be viewed or edited.
    """
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]
    # queryset = Sample.objects.all()

    def get_queryset(self): # type: ignore
        """
        This view should only return samples owned by the currently authenticated user.
        """
        return Sample.objects.filter(owner=self.request.user).prefetch_related('tasks', 'audit_logs')

    def perform_create(self, serializer):
        """
        Set the owner of the new sample to the logged-in user.
        """
        sample = serializer.save(owner=self.request.user)
        AuditLog.objects.create(
            sample=sample,
            actor=self.request.user,
            action="Sample registered."
        )

    def perform_update(self, serializer):
        """
        Create an audit log when the sample is updated.
        """
        old_status = serializer.instance.status
        
        sample = serializer.save()
        
        if old_status != sample.status:
            AuditLog.objects.create(
                sample=sample,
                actor=self.request.user,
                action=f"Status changed from '{old_status}' to '{sample.status}'."
            )

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_sample(self):
        """Helper function to get the parent sample."""
        try:
            sample = Sample.objects.get(
                pk=self.kwargs['sample_pk'], owner=self.request.user
            )
            return sample
        except Sample.DoesNotExist:
            raise ValidationError("Sample not found.")

    def get_queryset(self): # type: ignore
        """This view should only return tasks for the specified sample."""
        sample = self.get_sample()
        return Task.objects.filter(sample=sample)

    def perform_create(self, serializer):
        """
        Link the new task to the sample from the URL.
        The serializer now handles the 'analyst' ID automatically.
        """
        sample = self.get_sample()
        serializer.save(sample=sample)

class UserDetailView(APIView):
    """
    API endpoint to get the current logged-in user's details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = ReadOnlyUserSerializer(request.user)
        return Response(serializer.data)