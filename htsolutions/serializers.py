from pkgutil import read_code

from black import TRANSFORMED_MAGICS
from .models import Color, Product, Category, Family, SubFamily, Brand, Attribute
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "name"]


class FamilySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Family
        fields = ["pk", "name", "category"]


class FamilySerializerPUTandPOST(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["pk", "name", "category"]


class SubFamilySerializer(serializers.ModelSerializer):
    family = FamilySerializer(many=False, read_only=True)

    class Meta:
        model = Family
        fields = ["pk", "name", "family"]


class SubFamilySerializerPUTandPOST(serializers.ModelSerializer):
    class Meta:
        model = SubFamily
        fields = ["pk", "name", "family"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    subFamily = SubFamilySerializer(many=False, read_only=True)
    attribute = AttributeSerializer(many=True, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    color = ColorSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializerPUTandPOST(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
