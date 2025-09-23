from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
from django.utils import timezone
import google.generativeai as genai
import json
import logging
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from .models import UserProfile, EmailRequest, EmailSent

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)


@api_view(['POST'])
def generate_email(request):
    """
    Generate job application email using Google Gemini AI
    """
    try:
        # Validate required fields
        required_fields = ['hr_email', 'company', 'role', 'name', 'skills']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract data from request
        hr_email = request.data['hr_email']
        company = request.data['company']
        role = request.data['role']
        name = request.data['name']
        skills = request.data['skills']

        # Create email request record
        email_request = EmailRequest.objects.create(
            hr_email=hr_email,
            company=company,
            role=role,
            name=name,
            skills=skills
        )

        # Generate email using Gemini AI
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Write a professional job application email for the following details:
        
        Applicant Name: {name}
        Company: {company}
        Position: {role}
        HR Email: {hr_email}
        Skills: {skills}
        
        Please write a compelling, professional email that:
        1. Introduces the candidate professionally
        2. Highlights relevant skills and experience
        3. Expresses genuine interest in the company and role
        4. Includes a clear call to action
        5. Is concise but comprehensive (around 200-300 words)
        6. Uses a professional but engaging tone
        
        Format the email with proper subject line and body. Make it personalized and specific to the role and company.
        """

        try:
            response = model.generate_content(prompt)
            generated_email = response.text
            
            # Update the email request with generated content
            email_request.generated_email = generated_email
            email_request.save()
            
            return Response({
                'status': 'success',
                'email_text': generated_email,
                'request_id': email_request.id
            }, status=status.HTTP_200_OK)
            
        except Exception as ai_error:
            logger.error(f"Gemini AI error: {str(ai_error)}")
            
            # Fallback to template email if AI fails
            fallback_email = f"""Subject: Application for {role} Position at {company}

Dear Hiring Manager,

I am writing to express my strong interest in the {role} position at {company}. With my expertise in {skills}, I am confident that I would be a valuable addition to your team.

I am particularly excited about the opportunity to contribute to innovative projects and work alongside talented professionals at {company}. I would welcome the opportunity to discuss how my skills and passion for technology can contribute to your team's success.

Thank you for considering my application. I look forward to hearing from you soon.

Best regards,
{name}"""
            
            # Update the email request with fallback content
            email_request.generated_email = fallback_email
            email_request.save()
            
            return Response({
                'status': 'success',
                'email_text': fallback_email,
                'request_id': email_request.id,
                'warning': 'AI generation failed, using template email'
            }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Unexpected error in generate_email: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def send_email(request):
    """
    Send email via Django SMTP
    """
    try:
        # Validate required fields
        required_fields = ['hr_email', 'subject', 'body']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract data from request
        hr_email = request.data['hr_email']
        subject = request.data['subject']
        body = request.data['body']

        # Validate email configuration
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            return Response(
                {'error': 'Email configuration not set. Please configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Send email
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[hr_email],
                fail_silently=False,
            )
            
            # Record the sent email
            EmailSent.objects.create(
                to_email=hr_email,
                subject=subject,
                body=body,
                status='sent'
            )
            
            return Response({
                'status': 'sent',
                'message': 'Email sent successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as email_error:
            logger.error(f"Email sending error: {str(email_error)}")
            
            # Record failed email attempt
            EmailSent.objects.create(
                to_email=hr_email,
                subject=subject,
                body=body,
                status='failed'
            )
            
            return Response(
                {'error': f'Failed to send email: {str(email_error)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        logger.error(f"Unexpected error in send_email: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def create_user_profile(request):
    """
    Create or update user profile with comprehensive information
    """
    try:
        # Handle both JSON and multipart form data
        content_type = request.content_type or ''
        
        if 'multipart/form-data' in content_type:
            # Handle file upload with form data
            data = request.POST
        else:
            # Handle JSON data
            data = request.data
        
        # Extract basic information
        name = data.get('name')
        location = data.get('location')
        phone_number = data.get('phone_number')
        primary_email = data.get('primary_email')
        
        if not all([name, location, phone_number, primary_email]):
            return Response(
                {'error': 'Missing required fields: name, location, phone_number, primary_email'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if profile already exists
        profile, created = UserProfile.objects.get_or_create(
            primary_email=primary_email,
            defaults={
                'name': name,
                'location': location,
                'phone_number': phone_number,
                'alternative_email': data.get('alternative_email'),
                'portfolio_url': data.get('portfolio_url'),
                'linkedin_url': data.get('linkedin_url'),
                'github_url': data.get('github_url'),
                'leetcode_url': data.get('leetcode_url'),
                'education_degree': data.get('education_degree'),
                'education_field': data.get('education_field'),
                'university_name': data.get('university_name'),
                'graduation_year': data.get('graduation_year'),
                'gpa': data.get('gpa'),
                'programming_languages': data.get('programming_languages'),
                'python_frameworks': data.get('python_frameworks'),
                'frontend_technologies': data.get('frontend_technologies'),
                'mobile_development': data.get('mobile_development'),
                'databases': data.get('databases'),
                'cloud_devops': data.get('cloud_devops'),
                'deployment_platforms': data.get('deployment_platforms'),
                'integrations': data.get('integrations'),
                'development_practices': data.get('development_practices'),
                'professional_experience': data.get('professional_experience'),
                'projects': data.get('projects'),
            }
        )
        
        if not created:
            # Update existing profile
            profile.name = name
            profile.location = location
            profile.phone_number = phone_number
            profile.alternative_email = data.get('alternative_email')
            profile.portfolio_url = data.get('portfolio_url')
            profile.linkedin_url = data.get('linkedin_url')
            profile.github_url = data.get('github_url')
            profile.leetcode_url = data.get('leetcode_url')
            profile.education_degree = data.get('education_degree')
            profile.education_field = data.get('education_field')
            profile.university_name = data.get('university_name')
            profile.graduation_year = data.get('graduation_year')
            profile.gpa = data.get('gpa')
            profile.programming_languages = data.get('programming_languages')
            profile.python_frameworks = data.get('python_frameworks')
            profile.frontend_technologies = data.get('frontend_technologies')
            profile.mobile_development = data.get('mobile_development')
            profile.databases = data.get('databases')
            profile.cloud_devops = data.get('cloud_devops')
            profile.deployment_platforms = data.get('deployment_platforms')
            profile.integrations = data.get('integrations')
            profile.development_practices = data.get('development_practices')
            profile.professional_experience = data.get('professional_experience')
            profile.projects = data.get('projects')
            profile.save()
        
        # Handle resume file upload
        if 'resume_file' in request.FILES:
            profile.resume_file = request.FILES['resume_file']
            profile.save()
        
        return Response({
            'status': 'success',
            'message': 'Profile created' if created else 'Profile updated',
            'profile_id': profile.id,
            'created': created
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error in create_user_profile: {str(e)}")
        logger.error(f"Request content type: {request.content_type}")
        logger.error(f"Request method: {request.method}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def generate_email_enhanced(request):
    """
    Generate job application email using comprehensive user profile data
    """
    try:
        # Get profile_id or create from request data
        profile_id = request.data.get('profile_id')
        
        if profile_id:
            try:
                user_profile = UserProfile.objects.get(id=profile_id)
            except UserProfile.DoesNotExist:
                return Response(
                    {'error': 'User profile not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Create profile from request data (backward compatibility)
            return Response(
                {'error': 'profile_id is required. Please create a user profile first using /api/create-profile/'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract job details
        hr_email = request.data.get('hr_email')
        company = request.data.get('company')
        role = request.data.get('role')
        job_description = request.data.get('job_description', '')
        
        if not all([hr_email, company, role]):
            return Response(
                {'error': 'Missing required fields: hr_email, company, role'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create email request
        email_request = EmailRequest.objects.create(
            user_profile=user_profile,
            hr_email=hr_email,
            company=company,
            role=role,
            job_description=job_description
        )
        
        # Generate comprehensive email using Gemini AI
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Build comprehensive prompt with all user data
        prompt = f"""
        Write a SHORT and SWEET professional job application email (maximum 150 words) for the following candidate:
        
        CANDIDATE:
        Name: {user_profile.name}
        Education: {user_profile.education_degree} in {user_profile.education_field} from {user_profile.university_name} ({user_profile.graduation_year})
        Key Skills: {user_profile.programming_languages}
        Experience: {user_profile.professional_experience[:200]}...
        Projects: {user_profile.projects[:150]}...
        Portfolio: {user_profile.portfolio_url or 'N/A'}
        LinkedIn: {user_profile.linkedin_url or 'N/A'}
        GitHub: {user_profile.github_url or 'N/A'}
        
        JOB DETAILS:
        Company: {company}
        Position: {role}
        Job Description: {job_description}
        
        Write a BRIEF email that:
        1. Introduces candidate in 1-2 sentences
        2. Highlights 2-3 most relevant skills/achievements
        3. Shows interest in the role
        4. Includes professional signature with contact info
        5. Keep it under 150 words - be concise and impactful
        6. Include subject line
        
        Make it professional but brief - hiring managers are busy!
        """
        
        try:
            response = model.generate_content(prompt)
            generated_email = response.text
            
            # Update the email request with generated content
            email_request.generated_email = generated_email
            email_request.save()
            
            return Response({
                'status': 'success',
                'email_text': generated_email,
                'request_id': email_request.id,
                'profile_id': user_profile.id
            }, status=status.HTTP_200_OK)
            
        except Exception as ai_error:
            logger.error(f"Gemini AI error: {str(ai_error)}")
            
            # Short and sweet fallback email
            fallback_email = f"""Subject: Application for {role} Position at {company}

Dear Hiring Manager,

I am {user_profile.name}, a {user_profile.education_degree} graduate in {user_profile.education_field} from {user_profile.university_name}. I am excited to apply for the {role} position at {company}.

My key qualifications include:
• Strong skills in {user_profile.programming_languages}
• {user_profile.professional_experience[:100]}{'...' if len(user_profile.professional_experience) > 100 else ''}

I am passionate about contributing to {company}'s innovative projects and would love to discuss how my skills can benefit your team.

Best regards,
{user_profile.name}
{user_profile.phone_number}
{user_profile.primary_email}"""
            
            # Update the email request with fallback content
            email_request.generated_email = fallback_email
            email_request.save()
            
            return Response({
                'status': 'success',
                'email_text': fallback_email,
                'request_id': email_request.id,
                'profile_id': user_profile.id,
                'warning': 'AI generation failed, using enhanced template email'
            }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Unexpected error in generate_email_enhanced: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def send_email_with_resume(request):
    """
    Send email with resume attachment
    """
    try:
        # Validate required fields
        required_fields = ['hr_email', 'subject', 'body', 'profile_id']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract data from request
        hr_email = request.data['hr_email']
        subject = request.data['subject']
        body = request.data['body']
        profile_id = request.data['profile_id']
        
        try:
            user_profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate email configuration
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            return Response(
                {'error': 'Email configuration not set. Please configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Create email with attachment support
            email = EmailMultiAlternatives(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[hr_email],
            )
            
            # Attach resume if available
            resume_attached = False
            if user_profile.resume_file:
                try:
                    email.attach_file(user_profile.resume_file.path)
                    resume_attached = True
                except Exception as attach_error:
                    logger.warning(f"Failed to attach resume: {str(attach_error)}")
            
            email.send()
            
            # Record the sent email
            EmailSent.objects.create(
                to_email=hr_email,
                subject=subject,
                body=body,
                status='sent',
                resume_attached=resume_attached
            )
            
            return Response({
                'status': 'sent',
                'message': 'Email sent successfully',
                'resume_attached': resume_attached
            }, status=status.HTTP_200_OK)
            
        except Exception as email_error:
            logger.error(f"Email sending error: {str(email_error)}")
            
            # Record failed email attempt
            EmailSent.objects.create(
                to_email=hr_email,
                subject=subject,
                body=body,
                status='failed',
                resume_attached=False
            )
            
            return Response(
                {'error': f'Failed to send email: {str(email_error)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        logger.error(f"Unexpected error in send_email_with_resume: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_user_profile(request, profile_id):
    """
    Get user profile by ID
    """
    try:
        profile = UserProfile.objects.get(id=profile_id)
        
        return Response({
            'status': 'success',
            'profile': {
                'id': profile.id,
                'name': profile.name,
                'location': profile.location,
                'phone_number': profile.phone_number,
                'primary_email': profile.primary_email,
                'alternative_email': profile.alternative_email,
                'portfolio_url': profile.portfolio_url,
                'linkedin_url': profile.linkedin_url,
                'github_url': profile.github_url,
                'leetcode_url': profile.leetcode_url,
                'education_degree': profile.education_degree,
                'education_field': profile.education_field,
                'university_name': profile.university_name,
                'graduation_year': profile.graduation_year,
                'gpa': float(profile.gpa) if profile.gpa else None,
                'programming_languages': profile.programming_languages,
                'python_frameworks': profile.python_frameworks,
                'frontend_technologies': profile.frontend_technologies,
                'mobile_development': profile.mobile_development,
                'databases': profile.databases,
                'cloud_devops': profile.cloud_devops,
                'deployment_platforms': profile.deployment_platforms,
                'integrations': profile.integrations,
                'development_practices': profile.development_practices,
                'professional_experience': profile.professional_experience,
                'projects': profile.projects,
                'has_resume': bool(profile.resume_file),
                'created_at': profile.created_at,
                'updated_at': profile.updated_at
            }
        }, status=status.HTTP_200_OK)
        
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_user_profile: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def generate_cover_letter_pdf(request):
    """
    Generate cover letter PDF using user profile and detailed job/company information
    """
    try:
        # Validate required fields
        required_fields = ['profile_id', 'company', 'role']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Get user profile
        profile_id = request.data['profile_id']
        company = request.data['company']
        role = request.data['role']
        job_description = request.data.get('job_description', '')
        
        # Optional detailed company information
        recipient_name = request.data.get('recipient_name', 'Hiring Manager')
        company_address = request.data.get('company_address', '')
        company_city_state_zip = request.data.get('company_city_state_zip', '')
        previous_company = request.data.get('previous_company', '')
        key_skills = request.data.get('key_skills', '')
        specific_achievements = request.data.get('specific_achievements', '')
        company_interest = request.data.get('company_interest', '')
        personal_qualities = request.data.get('personal_qualities', '')
        
        try:
            user_profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leading=12
        )
        
        # Build PDF content
        story = []
        
        # Header with compact format - no extra spacing
        story.append(Paragraph(f"{user_profile.name}", title_style))
        
        # Create compact contact info without extra spacing
        contact_info = f"{user_profile.location}<br/>{user_profile.primary_email}<br/>{user_profile.phone_number}"
        if user_profile.linkedin_url:
            contact_info += f"<br/>LinkedIn: {user_profile.linkedin_url}"
        if user_profile.github_url:
            contact_info += f"<br/>GitHub: {user_profile.github_url}"
        if user_profile.portfolio_url:
            contact_info += f"<br/>Portfolio: {user_profile.portfolio_url}"
        
        story.append(Paragraph(contact_info, normal_style))
        story.append(Spacer(1, 15))
        
        # Date
        story.append(Paragraph(f"{timezone.now().strftime('%B %d, %Y')}", normal_style))
        story.append(Spacer(1, 10))
        
        # Company info with full address if provided
        if company_address or company_city_state_zip:
            company_info = f"{recipient_name}<br/>{company}"
            if company_address:
                company_info += f"<br/>{company_address}"
            if company_city_state_zip:
                company_info += f"<br/>{company_city_state_zip}"
            story.append(Paragraph(company_info, normal_style))
        else:
            story.append(Paragraph(f"{recipient_name}<br/>{company}", normal_style))
        
        story.append(Spacer(1, 10))
        
        # Subject
        story.append(Paragraph(f"Subject: Application for the Position of {role}", heading_style))
        story.append(Spacer(1, 8))
        
        # Cover letter body using the detailed format - compact version
        greeting = f"Dear {recipient_name},"
        story.append(Paragraph(greeting, normal_style))
        story.append(Spacer(1, 6))
        
        # Introduction paragraph - more concise
        intro = f"I am writing to express my interest in the {role} position at {company}. With my background in {user_profile.education_field or 'software development'}, I am confident in my ability to contribute effectively to your team."
        story.append(Paragraph(intro, normal_style))
        story.append(Spacer(1, 6))
        
        # Experience and skills paragraph - more concise
        if previous_company or key_skills or specific_achievements:
            # Use provided details or fallback to profile data
            prev_company = previous_company or "my previous role"
            skills = key_skills or user_profile.programming_languages or "software development"
            achievements = specific_achievements[:150] + "..." if len(specific_achievements) > 150 else specific_achievements
            
            exp_text = f"In my previous role at {prev_company}, I developed strong skills in {skills}. {achievements} I am enthusiastic about bringing my expertise to support {company}'s goals."
        else:
            # Fallback to profile data - more concise
            exp_text = f"In my professional experience, I developed strong skills in {user_profile.programming_languages}. {user_profile.professional_experience[:120]}{'...' if len(user_profile.professional_experience) > 120 else ''} I am enthusiastic about contributing to {company}'s success."
        
        story.append(Paragraph(exp_text, normal_style))
        story.append(Spacer(1, 6))
        
        # Company interest paragraph - more concise
        if company_interest:
            interest_text = f"What excites me most about this opportunity is {company_interest}. I am eager to bring my {personal_qualities or 'technical skills and passion'} to your organization."
        else:
            interest_text = f"What excites me most about this opportunity is the chance to contribute to {company}'s innovative projects. I am eager to bring my {personal_qualities or 'technical skills and passion'} to your organization."
        
        story.append(Paragraph(interest_text, normal_style))
        story.append(Spacer(1, 6))
        
        # Closing paragraph - more concise
        closing = f"Please find my resume attached for your review. I would welcome the opportunity to discuss how my background fits your needs. Thank you for considering my application."
        story.append(Paragraph(closing, normal_style))
        story.append(Spacer(1, 12))
        
        # Signature
        signature = f"Sincerely,<br/><br/>{user_profile.name}"
        story.append(Paragraph(signature, normal_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Create filename
        filename = f"cover_letter_{user_profile.name.replace(' ', '_')}_{company.replace(' ', '_')}_{role.replace(' ', '_')}.pdf"
        filename = filename.replace(' ', '_').replace(',', '').replace('.', '')
        
        # Return PDF as response
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating cover letter PDF: {str(e)}")
        return Response(
            {'error': 'Failed to generate cover letter PDF'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def send_email_with_resume_and_cover_letter(request):
    """
    Send email with both resume and cover letter attachments
    """
    try:
        # Validate required fields
        required_fields = ['hr_email', 'subject', 'body', 'profile_id', 'company', 'role']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract data from request
        hr_email = request.data['hr_email']
        subject = request.data['subject']
        body = request.data['body']
        profile_id = request.data['profile_id']
        company = request.data['company']
        role = request.data['role']
        job_description = request.data.get('job_description', '')
        
        # Optional detailed company information for cover letter
        recipient_name = request.data.get('recipient_name', 'Hiring Manager')
        company_address = request.data.get('company_address', '')
        company_city_state_zip = request.data.get('company_city_state_zip', '')
        previous_company = request.data.get('previous_company', '')
        key_skills = request.data.get('key_skills', '')
        specific_achievements = request.data.get('specific_achievements', '')
        company_interest = request.data.get('company_interest', '')
        personal_qualities = request.data.get('personal_qualities', '')
        
        try:
            user_profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate email configuration
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            return Response(
                {'error': 'Email configuration not set. Please configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Create email with attachment support
            email = EmailMultiAlternatives(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[hr_email],
            )
            
            attachments_added = []
            
            # Attach resume if available
            resume_attached = False
            if user_profile.resume_file:
                try:
                    email.attach_file(user_profile.resume_file.path)
                    resume_attached = True
                    attachments_added.append('Resume')
                except Exception as attach_error:
                    logger.warning(f"Failed to attach resume: {str(attach_error)}")
            
            # Generate and attach cover letter PDF
            try:
                # Create cover letter PDF
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
                
                styles = getSampleStyleSheet()
                
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=1
                )
                
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontSize=10,
                    spaceAfter=8,
                    leading=12
                )
                
                story = []
                
                # Header with compact format - no extra spacing
                story.append(Paragraph(f"{user_profile.name}", title_style))
                
                # Create compact contact info without extra spacing
                contact_info = f"{user_profile.location}<br/>{user_profile.primary_email}<br/>{user_profile.phone_number}"
                story.append(Paragraph(contact_info, normal_style))
                story.append(Spacer(1, 15))
                story.append(Paragraph(f"{timezone.now().strftime('%B %d, %Y')}", normal_style))
                story.append(Spacer(1, 10))
                
                # Company info with full address if provided
                if company_address or company_city_state_zip:
                    company_info = f"{recipient_name}<br/>{company}"
                    if company_address:
                        company_info += f"<br/>{company_address}"
                    if company_city_state_zip:
                        company_info += f"<br/>{company_city_state_zip}"
                    story.append(Paragraph(company_info, normal_style))
                else:
                    story.append(Paragraph(f"{recipient_name}<br/>{company}", normal_style))
                
                story.append(Spacer(1, 10))
                story.append(Paragraph(f"Subject: Application for the Position of {role}", normal_style))
                story.append(Spacer(1, 8))
                
                # Cover letter content using detailed format - compact version
                greeting = f"Dear {recipient_name},"
                story.append(Paragraph(greeting, normal_style))
                story.append(Spacer(1, 6))
                
                intro = f"I am writing to express my interest in the {role} position at {company}. With my background in {user_profile.education_field or 'software development'}, I am confident in my ability to contribute effectively to your team."
                story.append(Paragraph(intro, normal_style))
                story.append(Spacer(1, 6))
                
                # Experience and skills paragraph - more concise
                if previous_company or key_skills or specific_achievements:
                    prev_company = previous_company or "my previous role"
                    skills = key_skills or user_profile.programming_languages or "software development"
                    achievements = specific_achievements[:150] + "..." if len(specific_achievements) > 150 else specific_achievements
                    exp_text = f"In my previous role at {prev_company}, I developed strong skills in {skills}. {achievements} I am enthusiastic about bringing my expertise to support {company}'s goals."
                else:
                    exp_text = f"In my professional experience, I developed strong skills in {user_profile.programming_languages}. {user_profile.professional_experience[:120]}{'...' if len(user_profile.professional_experience) > 120 else ''} I am enthusiastic about contributing to {company}'s success."
                
                story.append(Paragraph(exp_text, normal_style))
                story.append(Spacer(1, 6))
                
                # Company interest paragraph - more concise
                if company_interest:
                    interest_text = f"What excites me most about this opportunity is {company_interest}. I am eager to bring my {personal_qualities or 'technical skills and passion'} to your organization."
                else:
                    interest_text = f"What excites me most about this opportunity is the chance to contribute to {company}'s innovative projects. I am eager to bring my {personal_qualities or 'technical skills and passion'} to your organization."
                
                story.append(Paragraph(interest_text, normal_style))
                story.append(Spacer(1, 6))
                
                closing = f"Please find my resume attached for your review. I would welcome the opportunity to discuss how my background fits your needs. Thank you for considering my application."
                story.append(Paragraph(closing, normal_style))
                story.append(Spacer(1, 12))
                
                signature = f"Sincerely,<br/><br/>{user_profile.name}"
                story.append(Paragraph(signature, normal_style))
                
                doc.build(story)
                buffer.seek(0)
                
                # Attach cover letter
                cover_letter_filename = f"cover_letter_{user_profile.name.replace(' ', '_')}_{company.replace(' ', '_')}.pdf"
                cover_letter_filename = cover_letter_filename.replace(' ', '_').replace(',', '').replace('.', '')
                
                email.attach(cover_letter_filename, buffer.getvalue(), 'application/pdf')
                attachments_added.append('Cover Letter')
                
            except Exception as cover_letter_error:
                logger.warning(f"Failed to generate cover letter: {str(cover_letter_error)}")
            
            email.send()
            
            # Record the sent email
            EmailSent.objects.create(
                to_email=hr_email,
                subject=subject,
                body=body,
                status='sent',
                resume_attached=resume_attached
            )
            
            return Response({
                'status': 'sent',
                'message': 'Email sent successfully',
                'resume_attached': resume_attached,
                'cover_letter_attached': 'Cover Letter' in attachments_added,
                'attachments': attachments_added
            }, status=status.HTTP_200_OK)
            
        except Exception as email_error:
            logger.error(f"Email sending error: {str(email_error)}")
            
            # Record failed email attempt
            EmailSent.objects.create(
                to_email=hr_email,
                subject=subject,
                body=body,
                status='failed',
                resume_attached=False
            )
            
            return Response(
                {'error': f'Failed to send email: {str(email_error)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        logger.error(f"Unexpected error in send_email_with_resume_and_cover_letter: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    """
    return Response({
        'status': 'healthy',
        'message': 'JobMailer API is running'
    }, status=status.HTTP_200_OK)
