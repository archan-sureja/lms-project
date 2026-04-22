from rest_framework.serializers import ModelSerializer 
from .models import Course , Topic

class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course 
        fields = "__all__"

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ("name","resource_link")

class CourseDetailSerializer(ModelSerializer):
    topics = TopicSerializer(many=True)
    class Meta:
        model = Course 
        fields = ('title','description','instructor','tags','allowed_depts','allowed_levels','topics')

