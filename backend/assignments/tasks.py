from celery import shared_task 
from django.core.mail import EmailMessage  
from datetime import timezone,timedelta
from .models import Assignment, Submission 
@shared_task
def send_deadline_reminders_task():
    now = timezone.now()
    upcoming_deadline = now + timedelta(days=2)
    assignments = Assignment.objects.filter(deadline__gt=now, deadline__lte=upcoming_deadline)
    for assignment in assignments:
        enrolled_users = [enrollment.user for enrollment in assignment.course.enrollments.select_related('user')]
        submitted_user_ids = set(Submission.objects.filter(assignment=assignment).values_list('submitted_by_id', flat=True))
        users_to_remind = [user for user in enrolled_users if user.id not in submitted_user_ids]
        for user in users_to_remind:
            EmailMessage(
                subject=f"Action Required: Assignment '{assignment.title}' is due soon!",
                message=f"Hi {user.username},\n\nThis is a friendly reminder to submit your assignment '{assignment.title}' before the deadline on {assignment.deadline.strftime('%b %d, %Y')}.",
                recipient_list=[user.email]
            ).send()