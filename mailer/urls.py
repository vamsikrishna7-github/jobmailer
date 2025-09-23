from django.urls import path
from . import views

urlpatterns = [
    # Legacy endpoints (for backward compatibility)
    path('api/generate-email/', views.generate_email, name='generate_email'),
    path('api/send-email/', views.send_email, name='send_email'),
    
    # Enhanced endpoints
    path('api/create-profile/', views.create_user_profile, name='create_user_profile'),
    path('api/generate-email-enhanced/', views.generate_email_enhanced, name='generate_email_enhanced'),
    path('api/send-email-with-resume/', views.send_email_with_resume, name='send_email_with_resume'),
    path('api/get-profile/<int:profile_id>/', views.get_user_profile, name='get_user_profile'),
    
    # Cover letter endpoints
    path('api/generate-cover-letter-pdf/', views.generate_cover_letter_pdf, name='generate_cover_letter_pdf'),
    path('api/send-email-with-resume-and-cover-letter/', views.send_email_with_resume_and_cover_letter, name='send_email_with_resume_and_cover_letter'),
    
    # Health check
    path('api/health/', views.health_check, name='health_check'),
]
