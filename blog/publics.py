#### SIgnals part ####

from blog import signals
def publish_blog():
    # publish blog logic
    signals.notify_author.send(sender=None, blog_id=123)