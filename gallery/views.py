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
        category = self.kwargs.get('category')
        print(category)
        if category:
            return Image.objects.filter(category__name__iexact=category).order_by('order')
        return Image.objects.all().order_by('order')
