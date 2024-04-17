from django.db import models
from datetime import datetime

class User(models.Model):
    name = models.CharField(blank=False, max_length=100)
    email = models.EmailField(blank=False)
    telephone = models.IntegerField(blank=False, max_length=15)
    address = models.CharField(max_length=200)
    data_registered = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Username: {self.name}, Email: {self.email}, Data registration: {self.data_registered}'

class Product(models.Model):
    name = models.CharField(blank=False, max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    data_addition = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True, default=None)

    def __str__(self):
        return f'Product name: {self.name}, Description: {self.description}, Price: {self.price}, Data addition: {self.data_addition}'


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

# Create your models here.
