from django.db import models

# Create your models here.

class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email_address=models.EmailField( max_length=254)
    address = models.TextField(max_length=500)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/',default=True)

    def __str__(self):
        return self.firstname
    