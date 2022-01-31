
from calendar import TUESDAY
from .models import Product, Category, Family, SubFamily, Brand, Attribute
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']

class FamilySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Family
        fields = ['pk', 'name', 'category']

class SubFamilySerializer(serializers.ModelSerializer):
    family = FamilySerializer(many=False, read_only=True)
    class Meta:
        model = SubFamily
        fields = ['pk', 'name', 'family']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    subFamily = SubFamilySerializer(many=False, read_only=True)
    attribute = AttributeSerializer(many=True, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'