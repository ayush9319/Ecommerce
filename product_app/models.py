from django.db import models
from core.models import Customer
# Create your models here.

class Product(models.Model):
    type = [
        ('Electronics','Electronics'),
        ('Clothing','Clothing'),
        ('Books','Books'),
        ('Toys','Toys'),
        ('Home Furniture','Home Furniture'),
    ]
    name = models.CharField(max_length=100, unique=True)
    descr = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100, choices=type)
    image = models.ImageField(upload_to='uploads/',default=True)
    

    def __str__(self):
        return self.name
    @property
    def total_price(self):
        return self.price

    class Meta:
        ordering = ['name']
        verbose_name = "Product Item"

class Order(models.Model):
    type = [
        ('placed', 'placed'),
        ('out_for_delivery', 'out_for_delivery'),
        ('in_transit', 'in_transit'),
        ('delivered', 'delivered'), 
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) 
    total_amount = models.IntegerField()
    status = models.CharField(max_length=100, choices=type)

    