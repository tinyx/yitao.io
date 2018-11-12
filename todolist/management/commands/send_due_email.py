from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from todolist.models import Event
from datetime import date, timedelta
from django.core.mail import send_mail
ALERT_DAYS = [timedelta(-1), timedelta(0), timedelta(1), timedelta(7), timedelta(30)]

class Command(BaseCommand):
    help = """This is a cron job for sending event due alert email everyday.
            You should not run this manually."""
    def handle(self, *args, **options):
        for user in User.objects.all():
            for event in Event.objects.filter(eventclass__user=user):
                time_delta = event.duedate - date.today()
                if time_delta in ALERT_DAYS:
                    if time_delta < timedelta(0):
                        subject = 'Event dued'
                        message = 'Your event %s dued at %s.' % (event.content, event.duedate)
                    else:
                        subject = 'Event will due soon'
                        message = 'Your event %s will due at %s' % (event.content, event.duedate)
                    send_mail(subject, message, 'todo@crabfactory.com', [user.email])
        return
