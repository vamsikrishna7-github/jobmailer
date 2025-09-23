from django.contrib import admin
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.html import format_html
from .models import UserProfile, EmailRequest, EmailSent


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'education_degree', 'education_field', 'university_name', 'graduation_year', 'location']
    list_filter = ['education_degree', 'graduation_year', 'created_at']
    search_fields = ['name', 'university_name', 'education_field', 'primary_email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'phone_number', 'primary_email')
        }),
        ('Contact Information', {
            'fields': ('alternative_email', 'portfolio_url', 'linkedin_url', 'github_url', 'leetcode_url')
        }),
        ('Education', {
            'fields': ('education_degree', 'education_field', 'university_name', 'graduation_year', 'gpa')
        }),
        ('Skills', {
            'fields': ('programming_languages', 'python_frameworks', 'frontend_technologies', 'mobile_development', 'databases', 'cloud_devops', 'deployment_platforms', 'integrations', 'development_practices')
        }),
        ('Experience & Projects', {
            'fields': ('professional_experience', 'projects')
        }),
        ('Resume', {
            'fields': ('resume_file',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmailRequest)
class EmailRequestAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'company', 'role', 'hr_email', 'created_at', 'send_email_link']
    list_filter = ['company', 'created_at']
    search_fields = ['user_profile__name', 'company', 'role', 'hr_email']
    readonly_fields = ['created_at', 'updated_at', 'send_email_link']
    actions = ['send_emails_action']

    def get_name(self, obj):
        return obj.user_profile.name if obj.user_profile else obj.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user_profile__name'

    def send_email_link(self, obj):
        if obj.generated_email:
            return format_html(
                '<a class="button" href="send-email/{}/">Send Email</a>',
                obj.pk
            )
        return format_html('<span style="color: red;">No email generated</span>')
    
    send_email_link.short_description = 'Send Email'
    send_email_link.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-email/<int:email_id>/', self.admin_site.admin_view(self.send_email_view), name='send_email'),
        ]
        return custom_urls + urls

    def send_email_view(self, request, email_id):
        try:
            email_request = EmailRequest.objects.get(pk=email_id)
            
            if request.method == 'POST':
                subject = request.POST.get('subject', f'Application for {email_request.role} at {email_request.company}')
                body = request.POST.get('body', email_request.generated_email)
                
                if not body:
                    messages.error(request, 'Email body cannot be empty')
                    return render(request, 'admin/mailer/send_email.html', {
                        'email_request': email_request,
                        'title': f'Send Email to {email_request.hr_email}'
                    })
                
                try:
                    # Create email with attachment support
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email_request.hr_email],
                    )
                    
                    # Attach resume if available
                    resume_attached = False
                    if email_request.user_profile and email_request.user_profile.resume_file:
                        try:
                            email.attach_file(email_request.user_profile.resume_file.path)
                            resume_attached = True
                        except Exception as attach_error:
                            logger.warning(f"Failed to attach resume: {str(attach_error)}")
                    
                    email.send()
                    
                    # Record the sent email
                    EmailSent.objects.create(
                        email_request=email_request,
                        to_email=email_request.hr_email,
                        subject=subject,
                        body=body,
                        status='sent',
                        resume_attached=resume_attached
                    )
                    
                    messages.success(request, f'Email sent successfully to {email_request.hr_email}')
                    return redirect(f'/admin/mailer/emailrequest/{email_id}/change/')
                    
                except Exception as e:
                    messages.error(request, f'Failed to send email: {str(e)}')
            
            return render(request, 'admin/mailer/send_email.html', {
                'email_request': email_request,
                'title': f'Send Email to {email_request.hr_email}'
            })
            
        except EmailRequest.DoesNotExist:
            messages.error(request, 'Email request not found')
            return redirect('/admin/mailer/emailrequest/')

    def send_emails_action(self, request, queryset):
        sent_count = 0
        failed_count = 0
        
        for email_request in queryset:
            if not email_request.generated_email:
                failed_count += 1
                continue
                
            try:
                subject = f'Application for {email_request.role} at {email_request.company}'
                
                # Create email with attachment support
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=email_request.generated_email,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email_request.hr_email],
                )
                
                # Attach resume if available
                resume_attached = False
                if email_request.user_profile and email_request.user_profile.resume_file:
                    try:
                        email.attach_file(email_request.user_profile.resume_file.path)
                        resume_attached = True
                    except Exception as attach_error:
                        logger.warning(f"Failed to attach resume: {str(attach_error)}")
                
                email.send()
                
                # Record the sent email
                EmailSent.objects.create(
                    email_request=email_request,
                    to_email=email_request.hr_email,
                    subject=subject,
                    body=email_request.generated_email,
                    status='sent',
                    resume_attached=resume_attached
                )
                sent_count += 1
                
            except Exception as e:
                failed_count += 1
                messages.error(request, f'Failed to send email to {email_request.hr_email}: {str(e)}')
        
        if sent_count > 0:
            messages.success(request, f'Successfully sent {sent_count} email(s)')
        if failed_count > 0:
            messages.warning(request, f'Failed to send {failed_count} email(s)')
    
    send_emails_action.short_description = 'Send emails for selected requests'


@admin.register(EmailSent)
class EmailSentAdmin(admin.ModelAdmin):
    list_display = ['to_email', 'subject', 'sent_at', 'status', 'resume_attached', 'view_body_link']
    list_filter = ['status', 'sent_at', 'resume_attached']
    search_fields = ['to_email', 'subject']
    readonly_fields = ['sent_at']
    actions = ['resend_emails_action']

    def view_body_link(self, obj):
        return format_html(
            '<a class="button" href="view-body/{}/">View Body</a>',
            obj.pk
        )
    
    view_body_link.short_description = 'View Body'
    view_body_link.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('view-body/<int:email_id>/', self.admin_site.admin_view(self.view_body_view), name='view_email_body'),
            path('resend/<int:email_id>/', self.admin_site.admin_view(self.resend_email_view), name='resend_email'),
        ]
        return custom_urls + urls

    def view_body_view(self, request, email_id):
        try:
            email_sent = EmailSent.objects.get(pk=email_id)
            return render(request, 'admin/mailer/view_email_body.html', {
                'email_sent': email_sent,
                'title': f'Email Body - {email_sent.subject}'
            })
        except EmailSent.DoesNotExist:
            messages.error(request, 'Email not found')
            return redirect('/admin/mailer/emailsent/')

    def resend_email_view(self, request, email_id):
        try:
            email_sent = EmailSent.objects.get(pk=email_id)
            
            if request.method == 'POST':
                try:
                    send_mail(
                        subject=email_sent.subject,
                        message=email_sent.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email_sent.to_email],
                        fail_silently=False,
                    )
                    
                    # Update status
                    email_sent.status = 'sent'
                    email_sent.save()
                    
                    messages.success(request, f'Email resent successfully to {email_sent.to_email}')
                    return redirect('/admin/mailer/emailsent/')
                    
                except Exception as e:
                    email_sent.status = 'failed'
                    email_sent.save()
                    messages.error(request, f'Failed to resend email: {str(e)}')
            
            return render(request, 'admin/mailer/resend_email.html', {
                'email_sent': email_sent,
                'title': f'Resend Email to {email_sent.to_email}'
            })
            
        except EmailSent.DoesNotExist:
            messages.error(request, 'Email not found')
            return redirect('/admin/mailer/emailsent/')

    def resend_emails_action(self, request, queryset):
        resent_count = 0
        failed_count = 0
        
        for email_sent in queryset:
            try:
                send_mail(
                    subject=email_sent.subject,
                    message=email_sent.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email_sent.to_email],
                    fail_silently=False,
                )
                
                email_sent.status = 'sent'
                email_sent.save()
                resent_count += 1
                
            except Exception as e:
                email_sent.status = 'failed'
                email_sent.save()
                failed_count += 1
                messages.error(request, f'Failed to resend email to {email_sent.to_email}: {str(e)}')
        
        if resent_count > 0:
            messages.success(request, f'Successfully resent {resent_count} email(s)')
        if failed_count > 0:
            messages.warning(request, f'Failed to resend {failed_count} email(s)')
    
    resend_emails_action.short_description = 'Resend selected emails'
