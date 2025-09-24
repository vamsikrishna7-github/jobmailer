from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import UserProfile, Education, Experience, Project, Skill, SocialLinks, BasicInfo


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'name', 'user_type')
    search_fields = ('email', 'username', 'name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    search_fields = ('user__email', 'user__username')


admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(SocialLinks)
admin.site.register(BasicInfo)

# Register your models here.
