from django.db import models
from django.contrib.auth.models import User


class EventClass(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todolist_eventclass_user"
    )
    name = models.CharField(max_length=20)
    order = models.IntegerField()

    def __unicode__(self):
        return "%s:%s" % (self.user, self.name)

    @classmethod
    def get_classes_by_user(cls, user):
        """
        Return a list of eventclasses based on
        the given user id
        """
        return cls.objects.filter(user__pk=user)

    class Meta:
        verbose_name = "Event Class"
        verbose_name_plural = "Event Classes"


class Event(models.Model):
    eventclass = models.ForeignKey(EventClass, on_delete=models.CASCADE)
    order = models.IntegerField()
    priority = models.IntegerField(default=0)
    content = models.TextField()
    duedate = models.DateField()
    done = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.content)

    def to_dict(self):
        """
        Return the information of the event
        in the format of dictionary
        """
        return {
            "id": self.id,
            "order": self.order,
            "priority": self.priority,
            "content": self.content,
            "duedate": str(self.duedate),
            "done": self.done,
        }

    @classmethod
    def get_events_by_class(cls, eventclass):
        """
        Return a list of events based on the
        given eventclass id
        """
        return cls.objects.filter(eventclass__pk=eventclass)

    @classmethod
    def get_events_dict_by_class(cls, eventclass, done):
        """
        Return a list of events based on the
        given eventclass id
        """
        return [
            x.to_dict()
            for x in cls.objects.filter(eventclass__pk=eventclass)
            .filter(done=done)
            .order_by("order")
        ]

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
