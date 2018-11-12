from rest_framework import serializers

from gallery.models import Category, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'name_cn', 'order', 'is_full_size')


class ImageSerializer(serializers.ModelSerializer):
    image_file = serializers.SlugRelatedField(read_only=True, slug_field='url')

    class Meta:
        model = Image
        fields = (
            'id',
            'name',
            'description',
            'description_cn',
            'category',
            'order',
            'annotation',
            'image_file'
        )
