from django.db import models
from filer.fields.image import FilerImageField


class Image(models.Model):
    name = models.CharField(
        max_length=255, null=False, blank=False, help_text="The name of the image"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="The description that will appear under the image",
    )
    description_cn = models.TextField(
        null=True,
        blank=True,
        help_text="The description that will appear under the image",
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, help_text="The category of this image"
    )
    order = models.IntegerField(
        default=0,
        null=False,
        blank=False,
        help_text="The order of this image under the category",
    )
    annotation = models.TextField(
        null=True,
        blank=True,
        help_text="Write something to remind you which image this is",
    )
    image_file = FilerImageField(
        null=False,
        blank=False,
        max_length=5000,
        on_delete=models.CASCADE,
        help_text="The image file",
    )

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=255, null=False, blank=False, help_text="The name of the category"
    )
    name_cn = models.CharField(
        max_length=255, null=False, blank=False, help_text="The name of the category"
    )
    order = models.IntegerField(
        default=0, null=False, blank=False, help_text="The order of this category"
    )
    is_full_size = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        help_text="Should this category be rendered full zied.",
    )

    def __unicode__(self):
        return self.name
