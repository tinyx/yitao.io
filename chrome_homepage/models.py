from django.db import models
from django.contrib.auth.models import User

from filer.fields.image import FilerImageField


class Website(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    url = models.URLField()
    thumbnail = FilerImageField(max_length=5000)

    def __unicode__(self):
        return '%s:%s' % (self.owner, self.name)

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'
