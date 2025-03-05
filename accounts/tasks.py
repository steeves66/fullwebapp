from fullwebapp.celery import app
from fullwebapp.celery import task
from celery.schedules import crontab

@app.on_after_finalize.connect
def setup_basic_periodic_tasks(sender, **kwargs):
   sender.add_periodic_task(
      crontab(),
      demo_task("periodic task")
   )

@task(bind=True)
def demo_task(self, value):
   print(value)