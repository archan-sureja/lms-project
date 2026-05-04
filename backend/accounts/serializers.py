from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers 
from django.contrib.auth.password_validation import validate_password
from .models import Department , Level
from .models import User
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Wrong password")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department 
        fields = "__all__"

class LevelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='level')
    class Meta:
        model = Level 
        fields = ("id","name",)
class UserProfileSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    def get_department(self,user):
        return user.employee_profile.department.name
    def get_level(self,user):
        return user.employee_profile.level.level
    class Meta:
        model = User
        fields = ('first_name',"last_name","username","email","role","department","level")
