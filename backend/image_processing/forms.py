from django import forms

from .models import Image


# ImageForm class for creating a form for the Image model
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            'title',
            'path',
        ]
