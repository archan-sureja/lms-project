import os 
from celery import Celery 
from celery.schedules import crontab 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('lms_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-assignment-reminders': {
        'task': 'assignments.tasks.send_deadline_reminders_task',
        'schedule': crontab(hour=8, minute=0), 
    },
}
