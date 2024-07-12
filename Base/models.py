from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from uuid import uuid4

# Create your models here.

STATUS_CHOICES = (
    ('pending', 'pending'), # Left Value : Actual Value, Right Value : Displayed Value
    ('processing', 'processing'),
    ('completed', 'completed')
)

TYPE_CHOICES = (
    ('contact', 'contact'),
    ('feedback', 'feedback')
)

CONSULT_CHOICES = (
    ('home', 'home'),
    ('hospital', 'hospital')
)

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other')
)

APPROVED_STATUS = (
    ('pending', 'pending'),
    ('accept', 'accept'),
    ('reject', 'reject')
)

class Doctor(models.Model) : 
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='doctor')
    speciality = models.CharField(max_length= 100)
    experience = models.IntegerField()
    location = models.CharField(max_length= 100)
    phone = models.CharField(max_length= 10)

    def __str__(self) : 
        return f"{self.user.username}"

class Appointment(models.Model) : 
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null= True, related_name= 'user')
    doctor = models.ForeignKey(Doctor, on_delete= models.SET_NULL, null= True)
    date = models.DateField()
    time = models.TimeField()

    patientName = models.CharField(max_length= 100, blank= True)
    patientEmail = models.EmailField(max_length= 100, blank= True)

    patientProblem = models.CharField(max_length= 100, blank= True)
    patientLocation = models.CharField(max_length= 100, blank= True)

    # City
    patientCity = models.CharField(max_length= 100, blank= True)

    # State
    patientState = models.CharField(max_length= 100, blank= True)

    # Postal Code
    postalCode = models.CharField(max_length= 100, blank= True)

    phone = models.CharField(max_length= 100, blank= True)

    consultStatus = models.CharField(max_length= 50, choices= CONSULT_CHOICES, default= 'hospital')

    status = models.CharField(max_length= 50, choices= STATUS_CHOICES, default= 'pending')

    patientHeight = models.CharField(max_length= 50, blank= True)
    patientWeight = models.CharField(max_length= 50, blank= True)

    patientAge = models.IntegerField(default= 0)
    patientGender = models.CharField(max_length= 10, choices= GENDER_CHOICES, blank= True)

    patientApproved = models.CharField(max_length= 50, choices= APPROVED_STATUS, default= 'pending')

    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self) : 
        return f"{self.user.username}'s Appointment"
    


class Response(models.Model) : 
    name = models.CharField(max_length= 100)
    email = models.CharField(max_length= 100)
    message = models.TextField()
    type = models.CharField(max_length= 50, choices= TYPE_CHOICES) 



class Bill(models.Model) : 
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null= True)
    appointment = models.OneToOneField(Appointment, on_delete= models.SET_NULL, null= True)
    totalBill = models.FloatField(default= 0) # Doctor Approves The Appointment and Sets The Total Bill
    billDescription = models.TextField(default= '') # Describes About The Bill Information
    slug = models.SlugField(blank= True, null= True, unique= True)
    payBill = models.BooleanField(default= False)
    stripeId = models.CharField(max_length= 255, blank= True, null= True)

    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def save(self, *args, **kwargs) : 
        if self.slug is None : 
            self.slug = slugify(f"{self.user.username}'s bill {uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self) : 
        return f"{self.user.username}'s Bill"