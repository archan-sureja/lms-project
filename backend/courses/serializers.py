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
    def get_allowed_depts(self,course):
        lst = []
        for dept in course.allowed_depts.all():
            lst.append(dept.name)
        return lst 
    def get_allowed_levels(self,course):
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
    topics = TopicSerializer(many=True,required=False)
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
            },
            'tags':{
                'required':False
            }
        }
    def create(self, validated_data):
        topics_data = validated_data.pop('topics',[])
        tags_data = validated_data.pop('tags',[])
        allowed_depts = validated_data.pop('allowed_depts',[])
        allowed_levels = validated_data.pop('allowed_levels',[])
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
            },
            "user":{
                "read_only":True
            }
        }
    
    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user 
        course = attrs.get('course')

        enrollment = Enrollment.objects.filter(user=user,course=course)
        if enrollment:
            raise serializers.ValidationError("user is already enrolled in given course")
        
        emp_profile = user.employee_profile
        print(course.allowed_depts.exists())
        if course.allowed_depts.exists():
            if emp_profile.department not in course.allowed_depts.all():
                raise serializers.ValidationError("given user's department is not allowed to enroll")
        
        if course.allowed_levels.exists():
            if emp_profile.level not in course.allowed_levels.all():
                raise serializers.ValidationError("given user's level is not allowed to enroll")
        
        return attrs 
    
class EnrollmentReadOnlySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    department = serializers.CharField(source='user.employee_profile.department',read_only=True)
    level = serializers.CharField(source='user.employee_profile.level',read_only=True)
    class Meta:
        model = Enrollment
        fields = ("user","course","enrolled_at","department","level")
        