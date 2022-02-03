import errno
from http.client import responses
from unicodedata import category
from black import NothingChanged
from django.http import Http404, JsonResponse
from django.shortcuts import render
import requests
from htsolutions.models import Category, Family, SubFamily, Product, Brand, Attribute
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core import serializers
from .serializers import (
    AttributeSerializer,
    BrandSerializer,
    CategorySerializer,
    FamilySerializer,
    FamilySerializerPUTandPOST,
    ProductSerializer,
    ProductSerializerPUTandPOST,
    SubFamilySerializer,
    SubFamilySerializerPUTandPOST,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def response_200(serializer):
    return openapi.Response("OK", serializer)


def response_201(serializer):
    return openapi.Response("Successful operation", serializer)


def response_204(serializer):
    return openapi.Response("Successful operation")


def response_404(serializer):
    return openapi.Response("Not Found")


def response_400(serializer):
    return openapi.Response("Bad Request")


# Create your views here.
@login_required
def index(request):
    """View function for home page of site."""

    # Generate count of all products
    responseProducts = requests.get(
        "http://127.0.0.1:8000/hometechsolutions/api/products/"
    )
    products = len(responseProducts.json())

    # Count Out of Stock products (status = '3')
    responseProducts = requests.get(
        "http://127.0.0.1:8000/hometechsolutions/api/products/"
    )
    if responseProducts.status_code != 200:
        return "error"
    products = len(responseProducts.json())
    outOfStockProducts = Product.objects.filter(stockStatus="3").count()

    # Count In Stock products (status = '1')
    inStockProducts = Product.objects.filter(stockStatus="1").count()

    # Count By order products (status = '2')
    byOrderProducts = Product.objects.filter(stockStatus="2").count()

    context = {
        "products": products,
        "inStockProducts": inStockProducts,
        "byOrderProducts": byOrderProducts,
        "outOfStockProducts": outOfStockProducts,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    context_object_name = "product_list"  # Name for the list as a template variable
    queryset = Product.objects.all  # Gets all products
    template_name = "product_list.html"  # Template name/location


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product_detail.html"  # Template name/location


@login_required
def productListByBrand(request, pk):
    products = Product.objects.filter(brand=pk)
    context = {"products_brand_list": products}
    return render(request, "products_brand_list.html", context)


####################### API ENDPOINTS #######################

# All products API JSON
class ProductsListAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get products",
        operation_description="Get all products",
        responses={status.HTTP_200_OK: response_200(ProductSerializer(many=True))},
    )
    def get(self, request, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Create product",
        operation_description="Create a new product",
        request_body=ProductSerializerPUTandPOST,
        responses={
            status.HTTP_201_CREATED: response_201(ProductSerializerPUTandPOST),
            status.HTTP_400_BAD_REQUEST: response_400(ProductSerializerPUTandPOST),
        },
    )
    def post(self, request, format=None):
        product = ProductSerializerPUTandPOST(data=request.data)
        if product.is_valid():
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)


# Product by ID
class ProductDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get product by id",
        operation_description="Get a specific product",
        responses={
            status.HTTP_200_OK: response_200(ProductSerializer),
            status.HTTP_404_NOT_FOUND: response_404(ProductSerializer),
        },
    )
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Update product",
        operation_description="Edit a specific product",
        request_body=ProductSerializerPUTandPOST,
        responses={
            status.HTTP_200_OK: response_200(ProductSerializerPUTandPOST),
            status.HTTP_400_BAD_REQUEST: response_400(ProductSerializerPUTandPOST),
            status.HTTP_404_NOT_FOUND: response_404(ProductSerializerPUTandPOST),
        },
    )
    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializerPUTandPOST(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete product by id",
        operation_description="Delete a specific product",
        responses={
            status.HTTP_204_NO_CONTENT: response_204(ProductSerializerPUTandPOST),
            status.HTTP_404_NOT_FOUND: response_404(ProductSerializerPUTandPOST),
        },
    )
    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# Products in stock API JSON
class ProductsInStockAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get products by 'in stock'",
        operation_description="Get all products with stock status in stock",
        rresponses={status.HTTP_200_OK: response_200(ProductSerializer(many=True))},
    )
    def get(self, request, format=None):
        product = Product.objects.filter(stockStatus=1)
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


# Products by order API JSON
class ProductsByOrderAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get product by 'by order'",
        operation_description="Get all products with stock status by order",
        responses={status.HTTP_200_OK: response_200(ProductSerializer(many=True))},
    )
    def get(self, request, format=None):
        product = Product.objects.filter(stockStatus=2)
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


# Products out of stock API JSON
class ProductsOutOfStockAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get product by 'out of stock'",
        operation_description="Get all products with stock status out of stock",
        responses={status.HTTP_200_OK: response_200(ProductSerializer(many=True))},
    )
    def get(self, request, format=None):
        product = Product.objects.filter(stockStatus=3)
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


# Category by ID
class CategoryDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get category by id",
        operation_description="Get a specific category",
        responses={
            status.HTTP_200_OK: response_200(CategorySerializer),
            status.HTTP_404_NOT_FOUND: response_404(CategorySerializer),
        },
    )
    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Update category",
        operation_description="Edit a specific category",
        request_body=CategorySerializer,
        responses={
            status.HTTP_200_OK: response_200(CategorySerializer),
            status.HTTP_400_BAD_REQUEST: response_400(CategorySerializer),
            status.HTTP_404_NOT_FOUND: response_404(CategorySerializer),
        },
    )
    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete category by id",
        operation_description="Delete a specific category",
        responses={
            status.HTTP_204_NO_CONTENT: response_204(CategorySerializer),
            status.HTTP_404_NOT_FOUND: response_404(CategorySerializer),
        },
    )
    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# Categories API JSON
class CategoriesAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get categories",
        operation_description="Get all categories",
        responses={status.HTTP_200_OK: response_200(CategorySerializer(many=True))},
    )
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Create category",
        operation_description="Create a new category",
        request_body=CategorySerializer,
        responses={
            status.HTTP_201_CREATED: response_201(CategorySerializer),
            status.HTTP_400_BAD_REQUEST: response_400(CategorySerializer),
        },
    )
    def post(self, request, format=None):
        category = CategorySerializer(data=request.data)
        if category.is_valid():
            category.save()
            return Response(category.data, status=status.HTTP_201_CREATED)
        return Response(category.errors, status=status.HTTP_400_BAD_REQUEST)


# Family by ID
class FamilyDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Family.objects.get(pk=pk)
        except Family.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get family by id",
        operation_description="Get a specific family",
        responses={
            status.HTTP_200_OK: response_200(FamilySerializer),
            status.HTTP_404_NOT_FOUND: response_404(FamilySerializer),
        },
    )
    def get(self, request, pk, format=None):
        family = self.get_object(pk)
        serializer = FamilySerializer(family)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Update family",
        operation_description="Edit a specific family",
        request_body=FamilySerializerPUTandPOST,
        responses={
            status.HTTP_200_OK: response_200(FamilySerializerPUTandPOST),
            status.HTTP_400_BAD_REQUEST: response_400(FamilySerializerPUTandPOST),
            status.HTTP_404_NOT_FOUND: response_404(FamilySerializerPUTandPOST),
        },
    )
    def put(self, request, pk, format=None):
        family = self.get_object(pk)
        serializer = FamilySerializerPUTandPOST(family, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete family by id",
        operation_description="Delete a specific family",
        responses={
            status.HTTP_204_NO_CONTENT: response_204(FamilySerializer),
            status.HTTP_404_NOT_FOUND: response_404(FamilySerializer),
        },
    )
    def delete(self, request, pk, format=None):
        family = self.get_object(pk)
        family.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# Families API JSON
class FamiliesAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get families",
        operation_description="Get all families",
        responses={status.HTTP_200_OK: response_200(FamilySerializer(many=True))},
    )
    def get(self, request, format=None):
        family = Family.objects.all()
        serializer = FamilySerializer(family, many=True)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Create family",
        operation_description="Create a new family",
        request_body=FamilySerializerPUTandPOST,
        responses={
            status.HTTP_201_CREATED: response_201(FamilySerializerPUTandPOST),
            status.HTTP_400_BAD_REQUEST: response_400(FamilySerializerPUTandPOST),
        },
    )
    def post(self, request, format=None):
        family = FamilySerializerPUTandPOST(data=request.data)
        if family.is_valid():
            family.save()
            return Response(family.data, status=status.HTTP_201_CREATED)
        return Response(family.errors, status=status.HTTP_400_BAD_REQUEST)


# SubFamily by ID
class SubFamilyDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return SubFamily.objects.get(pk=pk)
        except SubFamily.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get subfamily by id",
        operation_description="Get a specific subfamily",
        responses={
            status.HTTP_200_OK: response_200(SubFamilySerializer),
            status.HTTP_404_NOT_FOUND: response_404(SubFamilySerializer),
        },
    )
    def get(self, request, pk, format=None):
        subFamily = self.get_object(pk)
        serializer = SubFamilySerializer(subFamily)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Update subfamily",
        operation_description="Edit a specific subfamily",
        request_body=SubFamilySerializerPUTandPOST,
        responses={
            status.HTTP_200_OK: response_200(SubFamilySerializerPUTandPOST),
            status.HTTP_400_BAD_REQUEST: response_400(SubFamilySerializerPUTandPOST),
            status.HTTP_404_NOT_FOUND: response_404(SubFamilySerializerPUTandPOST),
        },
    )
    def put(self, request, pk, format=None):
        subFamily = self.get_object(pk)
        serializer = SubFamilySerializerPUTandPOST(subFamily, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete subfamily by id",
        operation_description="Delete a specific subfamily",
        responses={
            status.HTTP_204_NO_CONTENT: response_204(SubFamilySerializer),
            status.HTTP_404_NOT_FOUND: response_404(SubFamilySerializer),
        },
    )
    def delete(self, request, pk, format=None):
        subFamily = self.get_object(pk)
        subFamily.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# SubFamilies API JSON
class SubFamiliesAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get subfamilies",
        operation_description="Get all subfamilies",
        responses={status.HTTP_200_OK: response_200(SubFamilySerializer(many=True))},
    )
    def get(self, request, format=None):
        subFamily = SubFamily.objects.all()
        serializer = SubFamilySerializer(subFamily, many=True)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Create subfamily",
        operation_description="Create a new subfamily",
        request_body=SubFamilySerializerPUTandPOST,
        responses={
            status.HTTP_201_CREATED: response_201(SubFamilySerializerPUTandPOST),
            status.HTTP_400_BAD_REQUEST: response_400(SubFamilySerializerPUTandPOST),
        },
    )
    def post(self, request, format=None):
        subFamily = SubFamilySerializerPUTandPOST(data=request.data)
        if subFamily.is_valid():
            subFamily.save()
            return Response(subFamily.data, status=status.HTTP_201_CREATED)
        return Response(subFamily.errors, status=status.HTTP_400_BAD_REQUEST)


# Products by SubFamilie API JSON
class ProductsListBySubFamilyAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get products by subfamily id",
        operation_description="Get all products for a specific subfamily",
        responses={
            status.HTTP_200_OK: response_200(ProductSerializer(many=True)),
            status.HTTP_404_NOT_FOUND: response_404(ProductSerializer(many=True)),
        },
    )
    def get(self, request, pk, format=None):
        product = Product.objects.filter(subFamily=pk)
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


# Brand by ID
class BrandDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get brand by id",
        operation_description="Get a specific brand",
        responses={
            status.HTTP_200_OK: response_200(BrandSerializer),
            status.HTTP_404_NOT_FOUND: response_404(BrandSerializer),
        },
    )
    def get(self, request, pk, format=None):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Update brand",
        operation_description="Edit a specific brand",
        request_body=BrandSerializer,
        responses={
            status.HTTP_200_OK: response_200(BrandSerializer),
            status.HTTP_400_BAD_REQUEST: response_400(BrandSerializer),
            status.HTTP_404_NOT_FOUND: response_404(BrandSerializer),
        },
    )
    def put(self, request, pk, format=None):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete brand by id",
        operation_description="Delete a specific brand",
        responses={
            status.HTTP_204_NO_CONTENT: response_204(BrandSerializer),
            status.HTTP_404_NOT_FOUND: response_404(BrandSerializer),
        },
    )
    def delete(self, request, pk, format=None):
        brand = self.get_object(pk)
        brand.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# Brand API JSON
class BrandsAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get brands",
        operation_description="Get all brands",
        responses={status.HTTP_200_OK: response_200(BrandSerializer(many=True))},
    )
    def get(self, request, format=None):
        brand = Brand.objects.all()
        serializer = BrandSerializer(brand, many=True)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Create brand",
        operation_description="Create a new brand",
        request_body=BrandSerializer,
        responses={
            status.HTTP_201_CREATED: response_201(BrandSerializer),
            status.HTTP_400_BAD_REQUEST: response_400(BrandSerializer),
        },
    )
    def post(self, request, format=None):
        brand = BrandSerializer(data=request.data)
        if brand.is_valid():
            brand.save()
            return Response(brand.data, status=status.HTTP_201_CREATED)
        return Response(brand.errors, status=status.HTTP_400_BAD_REQUEST)


# Products by brand API JSON
class ProductsListByBrandAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get products by brand id",
        operation_description="Get all products for a specific brand",
        responses={
            status.HTTP_200_OK: response_200(ProductSerializer(many=True)),
            status.HTTP_404_NOT_FOUND: response_404(ProductSerializer(many=True)),
        },
    )
    def get(self, request, pk, format=None):
        product = Product.objects.filter(brand=pk)
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


# Attribute by ID
class AttributeDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Attribute.objects.get(pk=pk)
        except Attribute.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get attribute by id",
        operation_description="Get a specific attribute",
        responses={
            status.HTTP_200_OK: response_200(AttributeSerializer),
            status.HTTP_404_NOT_FOUND: response_404(AttributeSerializer),
        },
    )
    def get(self, request, pk, format=None):
        attribute = self.get_object(pk)
        serializer = AttributeSerializer(attribute)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Update attribute",
        operation_description="Edit a specific attribute",
        request_body=AttributeSerializer,
        responses={
            status.HTTP_200_OK: response_200(AttributeSerializer),
            status.HTTP_400_BAD_REQUEST: response_400(AttributeSerializer),
            status.HTTP_404_NOT_FOUND: response_404(AttributeSerializer),
        },
    )
    def put(self, request, pk, format=None):
        attribute = self.get_object(pk)
        serializer = AttributeSerializer(attribute, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete attribute by id",
        operation_description="Delete a specific attribute",
        responses={
            status.HTTP_204_NO_CONTENT: response_204(AttributeSerializer),
            status.HTTP_404_NOT_FOUND: response_404(AttributeSerializer),
        },
    )
    def delete(self, request, pk, format=None):
        brand = self.get_object(pk)
        brand.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# Attributes API JSON
class AttributesAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get attributes",
        operation_description="Get all attributes",
        responses={status.HTTP_200_OK: response_200(AttributeSerializer(many=True))},
    )
    def get(self, request, format=None):
        attribute = Attribute.objects.all()
        serializer = AttributeSerializer(attribute, many=True)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_summary="Create attribute",
        operation_description="Create a new attribute",
        request_body=AttributeSerializer,
        responses={
            status.HTTP_201_CREATED: response_201(AttributeSerializer),
            status.HTTP_400_BAD_REQUEST: response_400(AttributeSerializer),
        },
    )
    def post(self, request, format=None):
        attribute = AttributeSerializer(data=request.data)
        if attribute.is_valid():
            attribute.save()
            return Response(attribute.data, status=status.HTTP_201_CREATED)
        return Response(attribute.errors, status=status.HTTP_400_BAD_REQUEST)
