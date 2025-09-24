from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterViewSet, ProfileViewSet, EducationViewSet, ExperienceViewSet,
    ProjectViewSet, SkillViewSet, SocialLinksViewSet, AuthViewSet, BasicInfoViewSet
)


router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'links', SocialLinksViewSet, basename='links')
router.register(r'basic-info', BasicInfoViewSet, basename='basic-info')
router.register(r'auth', AuthViewSet, basename='auth')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

