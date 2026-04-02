from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from accounts.models import Profile
from jobs.models import Job, Category
from applications.models import Application
from .serializers import (
    UserSerializer, ProfileSerializer, RegisterSerializer,
    JobSerializer, JobCreateSerializer, CategorySerializer,
    ApplicationSerializer
)

# Authentication views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Profile views
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# Job views
class JobListView(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'job_type', 'location']
    search_fields = ['title', 'company', 'description']
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        return JobSerializer

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.profile)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

# Category views
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# Application views
class ApplicationListView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'job_seeker':
            return Application.objects.filter(applicant=user.profile)
        elif user.profile.role == 'employer':
            return Application.objects.filter(job__employer=user.profile)
        return Application.objects.none()

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user.profile)

class ApplicationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
