from django.contrib.auth.models import User
from rest_framework import serializers

from samples.models import AuditLog, Sample

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ReadOnlyUserSerializer(serializers.ModelSerializer):
    """
    A serializer for reading user data (no password)
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    
class AuditLogSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'actor_username', 'action', 'timestamp']

class SampleSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    audit_logs = AuditLogSerializer(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = [
            'id', 
            'sample_id', 
            'name', 
            'owner_username',
            'status', 
            'created_at', 
            'updated_at',
            'audit_logs'
        ]
        
    def create(self, validated_data):
        return Sample.objects.create(**validated_data)