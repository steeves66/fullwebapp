from django.dispatch import receiver
from blog import signals
from author import models
from django.db.models.signals import post_save

@receiver(signals.notify_author)
def send_email_to_author(sender, blog_id, **kwargs):
    # Send email to author 
    print("sending email to author logic", blog_id)

    
@receiver(post_save, sender=MyModel)
def my_handler(sender, **kwargs):
    print('my handle receiver')