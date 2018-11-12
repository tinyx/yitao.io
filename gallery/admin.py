from django.contrib import admin

from gallery.models import Image, Category


class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.StackedInline):
    extra = 0
    max_num = 0
    model = Image
    ordering = ("order",)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ImageInline,]


admin.site.register(Image)
admin.site.register(Category, CategoryAdmin)
