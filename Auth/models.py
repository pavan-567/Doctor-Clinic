from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import FileExtensionValidator

# Create your models here.
GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other')
)

USER_CHOICES = (
    ('doctor', 'doctor'),
    ('user', 'user')
)


class Profile(models.Model) : 
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    gender = models.CharField(max_length= 15, choices= GENDER_CHOICES)
    image = models.ImageField(default= 'profile.png', upload_to= 'profile', validators= [
        FileExtensionValidator(['png', 'jpg', 'jpeg'])
    ])
    role = models.CharField(max_length= 30, choices= USER_CHOICES, default= 'user')

    def __str__(self) : 
        return f"{self.user.username}'s profile"