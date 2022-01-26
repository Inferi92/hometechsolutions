from django.contrib import admin
from htsolutions.models import Category, Family, SubFamily, Product, Brand, Attribute
# Register your models here.
admin.site.register(Category)
admin.site.register(Family)
admin.site.register(SubFamily)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Attribute)