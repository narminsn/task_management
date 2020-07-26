# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import time
from .models import TaskModel
from datetime import datetime

@shared_task
def send_mail():
    data = TaskModel.objects.filter(expiration_date__year=datetime.now().year,
                                     expiration_date__month=datetime.now().month,
                                     expiration_date__day=datetime.now().day,
                                     expiration_date__hour=datetime.now().hour,
                                     expiration_date__minute=datetime.now().minute + 15)
    for field in data:
        email = field.user.email

        subject, from_email, to = 'Change password', settings.EMAIL_HOST_USER, email
        text_content = 'This is an important message.'
        html_content = """
                        <tr>
                            <td bgcolor="#ffffff" style="padding: 40px 40px; font-family: sans-serif; font-size: 15px; line-height: 20px; color: #555555; text-align: center;">
                                <p style="margin: 0;">Şifrənizi dəyişmək üçün aşağıdakı düyməni sıxın</p>
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#ffffff" style="padding: 0 40px 40px; font-family: sans-serif; font-size: 15px; line-height: 20px; color: #555555;">
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin: auto">
                                    <tr>
                                        <td style="border-radius: 3px; background: #20bdb7; text-align: center;" class="button-td">
                                            <a href="{}" style="background: #20bdb7; border: 15px solid #20bdb7; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;" class="button-a">
                                                &nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ffffff;">Şifrəni dəyiş</span>&nbsp;&nbsp;&nbsp;&nbsp;
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                <!-- Button : END -->
                            </td>
                        </tr>
                        """.format("http://localhost:8000")
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return "Success"



@shared_task
def toplama():
    time.sleep(20)
    return 2 + 3
