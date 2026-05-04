from rest_framework import serializers 
from .models import Assignment , Submission , SubmissionGrade 
from datetime import datetime , timezone , timedelta
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"

class AssignmentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id','course','title','description','deadline')
        extra_kwargs = {
            'id':{
                "read_only":True
            }
        }

    def validate(self,attr):
        deadline = attr.get('deadline')
        if deadline <= datetime.now(timezone.utc)+timedelta(days=1):
            raise serializers.ValidationError({"deadline":"minimum deadline must be 1 day"})
        return attr 

class SubmissionGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionGrade
        fields = ("id","submission","review_text","grade","graded_at")
        extra_kwargs = {
            "id":{
                "read_only":True
            },
            "submission":{
                "read_only":True
            },
            "graded_at":{
                "read_only":True
            }
        }

class SubmissionSerializer(serializers.ModelSerializer):
    is_late = serializers.SerializerMethodField()
    grade = SubmissionGradeSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    assignment = serializers.StringRelatedField()
    submitted_by = serializers.StringRelatedField()

    def get_is_late(self,submission):
        return submission.submitted_at > submission.assignment.deadline
    def get_file_url(self,submission):
        return f"http://localhost:8000/submissions/{submission.id}/download/"
    class Meta:
        model = Submission 
        fields = ("id","assignment","submitted_by","file_url","submitted_at","remarks","is_late","grade")

class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission 
        fields = ("id","assignment","submitted_by","file","submitted_at","remarks")
        extra_kwargs = {
            "id":{
                "read_only":True
            },
            "submitted_by":{
                "read_only":True
            },
            "submitted_at":{
                "read_only":True
            },
            "file":{
                "write_only":True
            }
        }
    def validate_file(self,value):
        extension = value.name.split(".")[-1] 
        if extension not in ["pdf","docx"]:
            raise serializers.ValidationError("Only .pdf, and .docx file formats are allowed")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size exceded limit of 5 MB")
        return value 
    
    def validate(self,attr):
        request = self.context.get('request')
        user = request.user 
        assignment = attr.get('assignment')
        
        if not user.enrollments.filter(course=assignment.course).exists():
            raise serializers.ValidationError("User must be enrolled to in course for submission")
    
        if Submission.objects.filter(submitted_by=user,assignment=assignment).exists():
            raise serializers.ValidationError("only one submission per assignment per user is allowed")

    
        return attr 
    
class SubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("id","assignment","submitted_by","file","submitted_at","remarks")
        extra_kwargs = {
            "id":{
                "read_only":True
            },
            "submitted_by":{
                "read_only":True
            },
            "submitted_at":{
                "read_only":True
            },
            "file":{
                "required":False
            },
            "assignment":{
                "required":False
            },
            "remarks":
            { "required":False }
        }
    def validate(self,attr):
        request = self.context.get('request',None)
        user = request.user 
        assignment = attr.get('assignment',None)
        
        if assignment and not user.enrollments.filter(course=assignment.course).exists():
            raise serializers.ValidationError("User must be enrolled to in course for submission")

        if assignment and assignment.deadline < datetime.now(timezone.utc):
            raise serializers.ValidationError("Deadline for this assignment has passed. You cannot update submission now.")
        return attr 



class SubmissionGradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionGrade
        fields = ("id","submission","review_text","grade","graded_at")
        extra_kwargs = {
            "id":{
                "read_only":True
            },
            "graded_at":{
                "read_only":True
            },
            "submission":
            {
                "read_only":True
            }
        }
    def validate(self,attrs):
        request = self.context.get('request',None)
        user = request.user 
        submission = attrs.get("submission",None)
        grade = attrs.get("grade",None)
        if submission and not submission.assignment.course.instructor != user:
            raise serializers.ValidationError("User only assign grade to thier learners")
        
        if grade<0 or grade>10:
            raise serializers.ValidationError({"grade":"grade must be between 0 to 10"})
        
        return attrs

