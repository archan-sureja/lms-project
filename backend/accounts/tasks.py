from celery import shared_task 
from django.core.mail import EmailMessage 

@shared_task
def send_credentials_email_task(user_email, username, raw_password, role):
    subject = f"Welcome to the LMS - Your {role.capitalize()} Account Details"
    message = f"""
    Hello {username},
    
    An admin has created a {role} account for you on the LMS.
    
    Here are your login credentials:
    Username: {username}
    Password: {raw_password}
    
    Please log in and change your password immediately.
    """
    return EmailMessage(subject=subject,body=message,to=[user_email])
