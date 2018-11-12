import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    life_partner_name = models.CharField(max_length=255, null=True, blank=True)
    anniversary_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
