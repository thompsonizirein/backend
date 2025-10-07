from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Label, Complaint, ContactMessage


@receiver(post_save, sender=Label)
def send_label_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Shiparama Logistics - New Label Created for {instance.track.tracking_id}"
        message = f"""Dear {instance.name},

We are pleased to inform you that a new shipment has been created for your tracking ID: {instance.track.tracking_id}
Your shipment is now being processed and is on its way. You can track the status of your items anytime on our website:
https://www.shiparama.org/

If you have any questions or need assistance, please do not hesitate to contact our customer support team.

Thank You,
Shiparama Logistics
"""
        recipient = instance.email

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            headers={'Reply-To': 'Shiparamexlogistics@post.com'}  # you can change this to any email
        )
        email.send(fail_silently=False)


@receiver(post_save, sender=Complaint)
def send_complaint_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Shiparama Logistics - New Complaint for {instance.track.tracking_id}"
        message = f"""Dear {instance.user_name},

A new complaint has been submitted for tracking ID {instance.track.tracking_id}.
Complaint Message:
{instance.message}

Please contact customer support to take action.

Best regards,
Shiparama Logistics
"""
        recipient = instance.email

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            headers={'Reply-To': 'Shiparamexlogistics@post.com'}
        )
        email.send(fail_silently=False)


@receiver(post_save, sender=ContactMessage)
def send_contact_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New Contact Message from {instance.name}"
        message = f"""Name: {instance.name}
Email: {instance.email}

Message:
{instance.message}
"""
        admin_email = settings.EMAIL_HOST_USER  # make sure this is set in settings.py

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
            headers={'Reply-To': 'Shiparamexlogistics@post.com'}
        )
        email.send(fail_silently=False)
