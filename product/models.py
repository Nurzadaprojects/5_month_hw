from django.db import models
from datetime import datetime
# Create your models here.
class Manager(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def birth_year(self):
        return datetime.now().year - self.age

class Color(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Product(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    color = models.ManyToManyField(Color, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


STARS = (
    (star, star * '* ') for star in range(1, 6)
)

class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=1)
    def __str__(self):
        return self.text


