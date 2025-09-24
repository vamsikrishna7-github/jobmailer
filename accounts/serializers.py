from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import UserProfile, Education, Experience, Project, Skill, SocialLinks, BasicInfo


User = get_user_model()


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = ['github', 'linkedin', 'portfolio', 'leetcode', 'codeforces', 'others']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'degree', 'institution', 'start_date', 'end_date', 'grade']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company_name', 'role', 'start_date', 'end_date', 'description']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tech_stack', 'link', 'github_link']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name', 'phone', 'user_type']
        read_only_fields = ['id', 'email', 'username', 'user_type']


class UserProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    social_links = SocialLinksSerializer(required=False)
    basic_info = serializers.SerializerMethodField(read_only=True)
    educations = EducationSerializer(many=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'profile_picture', 'bio', 'resume', 'skills',
            'social_links', 'basic_info', 'educations', 'experiences', 'projects',
            'updated_at', 'created_at'
        ]
        read_only_fields = ['updated_at', 'created_at']

    def _upsert_nested(self, instance, nested_key, serializer_cls, many, related_name=None):
        data = self.initial_data.get(nested_key)
        if data is None:
            return
        if many:
            manager = getattr(instance, nested_key)
            manager.all().delete()
            serializer = serializer_cls(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            for item in serializer.validated_data:
                serializer_cls.Meta.model.objects.create(profile=instance, **item)
        else:
            payload = data
            serializer = serializer_cls(data=payload)
            serializer.is_valid(raise_exception=True)
            obj, _ = serializer_cls.Meta.model.objects.get_or_create(profile=instance)
            for k, v in serializer.validated_data.items():
                setattr(obj, k, v)
            obj.save()

    def create(self, validated_data):
        skills_data = self.initial_data.get('skills')
        # Prevent accidental M2M direct assignment via validated_data
        validated_data.pop('skills', None)
        instance = UserProfile.objects.create(**validated_data)
        # Skills
        if skills_data:
            names = [s.get('name') for s in skills_data if s.get('name')]
            skill_objs = [Skill.objects.get_or_create(name=n.strip())[0] for n in names]
            instance.skills.set(skill_objs)
        # Nested
        self._upsert_nested(instance, 'social_links', SocialLinksSerializer, many=False)
        self._upsert_nested(instance, 'basic_info', BasicInfoSerializer, many=False)
        self._upsert_nested(instance, 'educations', EducationSerializer, many=True)
        self._upsert_nested(instance, 'experiences', ExperienceSerializer, many=True)
        self._upsert_nested(instance, 'projects', ProjectSerializer, many=True)
        return instance

    def update(self, instance, validated_data):
        skills_data = self.initial_data.get('skills')
        # Avoid direct assignment to M2M
        validated_data.pop('skills', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if skills_data is not None:
            names = [s.get('name') for s in skills_data if s.get('name')]
            skill_objs = [Skill.objects.get_or_create(name=n.strip())[0] for n in names]
            instance.skills.set(skill_objs)
        self._upsert_nested(instance, 'social_links', SocialLinksSerializer, many=False)
        self._upsert_nested(instance, 'basic_info', BasicInfoSerializer, many=False)
        self._upsert_nested(instance, 'educations', EducationSerializer, many=True)
        self._upsert_nested(instance, 'experiences', ExperienceSerializer, many=True)
        self._upsert_nested(instance, 'projects', ProjectSerializer, many=True)
        return instance

    def get_basic_info(self, obj):
        bi = getattr(obj, 'basic_info', None)
        if not bi:
            return None
        return BasicInfoSerializer(bi).data


class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = [
            'id', 'preferred_location', 'email', 'phone', 'alternate_email',
            'alternate_phone', 'address', 'email_app_user', 'email_app_password',
            'updated_at', 'created_at'
        ]
        read_only_fields = ['id', 'updated_at', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name', 'phone', 'user_type', 'password']
        read_only_fields = ['id', 'user_type']

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

