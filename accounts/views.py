from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Education, Experience, Project, Skill, SocialLinks, BasicInfo
from .serializers import (
    UserSerializer, RegisterSerializer, UserProfileSerializer, ChangePasswordSerializer,
    EducationSerializer, ExperienceSerializer, ProjectSerializer, SkillSerializer, SocialLinksSerializer,
    BasicInfoSerializer
)
from .permissions import IsOwnerProfile


User = get_user_model()


class RegisterViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=201)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').prefetch_related('skills')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfile]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = request.user.profile
        return Response(self.get_serializer(profile).data)

    @action(detail=False, methods=['post'], url_path='upload-resume')
    def upload_resume(self, request):
        profile = request.user.profile
        file = request.FILES.get('resume')
        if not file:
            return Response({'detail': 'No file provided'}, status=400)
        if not file.name.lower().endswith('.pdf'):
            return Response({'detail': 'Only PDF allowed'}, status=400)
        profile.resume = file
        profile.save()
        return Response({'detail': 'Resume uploaded', 'resume': profile.resume.url})


class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfile]

    def get_queryset(self):
        return Education.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfile]

    def get_queryset(self):
        return Experience.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfile]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'tech_stack']

    def get_queryset(self):
        return Project.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']


class SocialLinksViewSet(viewsets.ModelViewSet):
    serializer_class = SocialLinksSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfile]

    def get_queryset(self):
        return SocialLinks.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class BasicInfoViewSet(viewsets.ModelViewSet):
    serializer_class = BasicInfoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfile]

    def get_queryset(self):
        return BasicInfo.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'refresh token required'}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'detail': 'invalid token'}, status=400)
        return Response({'detail': 'logged out'})
