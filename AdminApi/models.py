from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class CustomUser(AbstractUser):
    user_type_choices=[
        ('Admin', 'Admin'),
        ('Bus Owner' ,'Bus Owner'),
        ('Passenger' ,'Passenger'),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices,default='Passenger')
    
    
class Admin(CustomUser):
    email_address=models.EmailField()                       
    
    
class BusOwner(CustomUser):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    proof=models.ImageField(upload_to="images",null=True,blank=True)
    is_approved=models.BooleanField(default="False")
    
    def __str__(self):
        return self.name
    

class Passenger(CustomUser):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email_address=models.EmailField()
    address=models.CharField(max_length=100)


    def __str__(self):
        return self.name
    



    
class Route(models.Model):
    name=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Busstop(models.Model):
    name=models.CharField(max_length=200)
    routes=models.ForeignKey(Route,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


class BusDriver(models.Model):
    busowner=models.ForeignKey(BusOwner,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    license=models.FileField(upload_to="license")
    age=models.IntegerField()
    dob=models.DateField()


    

class Bus(models.Model):
    busowner=models.ForeignKey(BusOwner,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images")
    Number_plate=models.CharField(max_length=500)
    Engine_no=models.IntegerField()
    RC_book=models.ImageField(upload_to="license",null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name



    

    


    

    

