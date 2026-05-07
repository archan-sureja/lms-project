from django.contrib import admin
from .models import Topic,Course , Tag, Enrollment 
# Register your models here.
class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1 

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course 
    inlines = [TopicInline]

admin.site.register(Tag)
admin.site.register(Enrollment)