from rest_framework import serializers 
from .models import Course , Topic , Enrollment 
class CourseListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Course 
        fields = ('id','title','description','tags')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("id","name","resource_link")
        extra_kwargs = {
            "id":{
                "read_only":True
            }
        }

class CourseDetailSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    allowed_depts = serializers.SerializerMethodField()
    allowed_levels = serializers.SerializerMethodField()
    tags = serializers.StringRelatedField(many=True)
    instructor = serializers.StringRelatedField()
    def get_allowedDepts(self,course):
        lst = []
        for dept in course.allowed_depts.all():
            lst.append(dept.name)
        return lst 
    def get_allowedLevels(self,course):
        lst = []
        for level in course.allowed_levels.all():
            lst.append(level.level)
        return lst
    class Meta:
        model = Course 
        fields = ('id','title','description','instructor','tags',
                  'allowed_depts','allowed_levels',
                  'topics')

class CourseDetailLearnerSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    instructor = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Course
        fields = ('id','title','description','instructor','tags','topics')

class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    instructor = serializers.StringRelatedField()
    class Meta:
        model = Course 
        fields = ('id','title','description','instructor','tags',
                  'allowed_depts','allowed_levels',
                  'topics')
        extra_kwargs = {
            'id':{
                'read_only':True
            },
            'instructor' :{
                'read_only':True
            }
        }
    def create(self, validated_data):
        topics_data = validated_data.pop('topics')
        tags_data = validated_data.pop('tags')
        allowed_depts = validated_data.pop('allowed_depts')
        allowed_levels = validated_data.pop('allowed_levels')
        course = Course.objects.create(**validated_data)
        course.allowed_depts.set(allowed_depts)
        course.allowed_levels.set(allowed_levels)
        course.tags.set(tags_data)
        for topic_data in topics_data:
            Topic.objects.create(course=course, **topic_data)
        return course

    def update(self, instance, validated_data):
        topics_data = validated_data.pop('topics',None)
        tags_data = validated_data.pop('tags',None)
        allowed_depts = validated_data.pop('allowed_depts',None)
        allowed_levels = validated_data.pop('allowed_levels',None)
        if validated_data:
            instance = super().update(instance,validated_data)
        
        if topics_data : 
            lst = []
            instance.topics.all().delete()
            for topic_data in topics_data:
                topic_data['course_id']=instance.id
                lst.append(Topic(**topic_data))
            Topic.objects.bulk_create(lst)
        if tags_data : 
            instance.tags.set(tags_data)
        if allowed_depts:
            instance.allowed_depts.set(allowed_depts)
        if allowed_levels:
            instance.allowed_levels.set(allowed_levels)
        return instance

class EnrollmentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment 
        fields = ("user","course","enrolled_at")
        extra_kwargs = {
            "enrolled_at" : {
                "read_only":True
            }
        }
    
    def validate(self, attrs):
        pass 

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    class Meta:
        model = Enrollment
        fields = ("user","course","enrolled_at")