from django.contrib import admin
from .models import Product, Condom, Gel

# Register your models here.
admin.site.register(Product)

admin.site.register(Condom)

admin.site.register(Gel)
