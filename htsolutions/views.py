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
from django.core import serializers as ser
from .serializers import AttributeSerializer, BrandSerializer, CategorySerializer, FamilySerializer, ProductSerializer, SubFamilySerializer

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
    template_name = "product_detail.html"  # Template name/location


@login_required
def productListByBrand(request, pk):
    products = Product.objects.filter(brand=pk)
    context = {"products_brand_list": products}
    return render(request, "products_brand_list.html", context)


####################### API ENDPOINTS #######################

# All products API JSON
class ProductsListView(APIView):
    def get(self, request, format=None):
        snippets = Product.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

class ProductDetailView(APIView):
    def get(self, request, pk, format=None):
        snippet = Product.objects.get(pk=pk)
        serializer = ProductSerializer(snippet, many=True)
        return JsonResponse(serializer.data, safe=False)

# Products in stock API JSON
class ProductsInStockView(APIView):
    def get(self, request, format=None):
        snippets = Product.objects.filter(stockStatus=1)
        serializer = ProductSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)


# Products by order API JSON
class ProductsByOrderView(APIView):
    def get(self, request, format=None):
        snippets = Product.objects.filter(stockStatus=2)
        serializer = ProductSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)


# Products out of stock API JSON
class ProductsOutOfStockView(APIView):
    def get(self, request, format=None):
        snippets = Product.objects.filter(stockStatus=3)
        serializer = ProductSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

# Categories API JSON
class CategoriesView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        categoriy = Category.objects.all()
        serializer = CategorySerializer(categoriy, many=True)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk, format=None):
        categoriy = self.get_object(pk)
        serializer = CategorySerializer(categoriy, data=request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Families API JSON
class FamiliesView(APIView):
    def get(self, request, format=None):
        snippets = Family.objects.all()
        serializer = FamilySerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

# SubFamilies API JSON
class SubFamiliesView(APIView):
    def get(self, request, format=None):
        snippets = SubFamily.objects.all()
        serializer = SubFamilySerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

#Products by SubFamilie API JSON
class ProductsListBySubFamily(APIView):
    def get(self, request, pk, format=None):
        snippets = Product.objects.filter(subFamily=pk)
        serializer = ProductSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

# Brand API JSON
class BrandsView(APIView):
    def get(self, request, format=None):
        snippets = Brand.objects.all()
        serializer = BrandSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)


# Products by brand API JSON
class ProductsListByBrand(APIView):
    def get(self, request, pk, format=None):
        snippets = Product.objects.filter(brand=pk)
        serializer = ProductSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

# Attributes API JSON
class AttributesView(APIView):
    def get(self, request, format=None):
        snippets = Attribute.objects.all()
        serializer = AttributeSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
