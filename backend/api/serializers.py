from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile
from jobs.models import Job, Category
from applications.models import Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, role=role)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    employer = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    applicant = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'