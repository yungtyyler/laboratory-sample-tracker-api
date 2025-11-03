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
    """
    API endpoint for viewing and editing tests associated with a sample.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # type: ignore
        """
        This view should only return tests for samples owned by the current user.
        """
        sample_pk = self.kwargs['sample_pk']
        
        return Task.objects.filter(
            sample__pk=sample_pk, 
            sample__owner=self.request.user
        )

    def perform_create(self, serializer):
        """
        Associate the new test with the sample from the URL.
        """
        sample_pk = self.kwargs['sample_pk']

        try:
            sample = Sample.objects.get(pk=sample_pk, owner=self.request.user)
        except Sample.DoesNotExist:
            raise ValidationError("Sample not found or you do not have permission.")
            
        serializer.save(sample=sample)

class UserDetailView(APIView):
    """
    API endpoint to get the current logged-in user's details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = ReadOnlyUserSerializer(request.user)
        return Response(serializer.data)