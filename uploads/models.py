from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ImageUpload(models.Model):
    name = models.CharField(max_length=100, help_text='Name of the image')
    image = models.ImageField(
        upload_to='images/', help_text='Image file to be uploaded')
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='uploads')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
