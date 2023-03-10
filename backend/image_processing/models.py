from django.db import models


# Image model for storing images
class Image(models.Model):
    title = models.CharField(max_length=50)
    path = models.ImageField(upload_to='images')
    asl_letter = models.CharField(max_length=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        output = f'id: {self.pk} - {self.title} - {self.path} - {self.asl_letter}'
        return output

    def get_path(self):
        return self.path.url
