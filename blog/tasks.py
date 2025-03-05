from blog import private
from fullwebapp.celery import task

@task(bind=True)
def send_email_to_followers(self, author_id, blog_id):
    print('sending email to all follower logic')