from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
import time


@shared_task
def generate_song(email:str):
    time.sleep(20)
    try:
        message = f"생성 완료 시간 : {timezone.now()}"
        mail_title = "[HappySong] 구매 알림 메일"
        sendEmail = EmailMessage(mail_title, message, settings.EMAIL_HOST_USER, to=[email])
        sendEmail.send()
    except:
        return False

    return True
