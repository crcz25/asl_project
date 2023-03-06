from rest_framework import serializers

from .models import Image


# Image Serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        ordering = ['updated_at']
