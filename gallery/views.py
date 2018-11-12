from rest_framework import generics

from gallery.models import Category, Image
from gallery.serializers import CategorySerializer, ImageSerializer


class CategoryListView(generics.ListAPIView):
    permission_classes = ()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all().order_by('order')


class ImageListView(generics.ListAPIView):
    permission_classes = ()
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.all().order_by('order')
