from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib import admin  
from django.db import models 
from django.urls import reverse
User._meta.get_field('email')._unique = True
#print(help(models.Model))
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile',verbose_name='username')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=200,blank=True)
    ban=models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super(Profile,self).save(*args,**kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
  

# Create your models here.
