from django.contrib import admin
from .models import Product, Manager, Color
from .models import Review
# Register your models here.

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Manager)
admin.site.register(Color)

