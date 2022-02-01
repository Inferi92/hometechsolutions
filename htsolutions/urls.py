from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from htsolutions import views



urlpatterns = [
    #URLS FRONTEND
    path("", views.index, name="index"),
    path("product/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/brand/<int:pk>", views.productListByBrand, name="products-brand-list"),

    #URLS API ENDPOINTS
    path("api/product/<int:pk>", views.ProductDetailView.as_view(), name="single_product"),
    path("api/products/", views.ProductsListView.as_view(), name="products_list_api"),
    path("api/products/inStock", views.ProductsInStockView.as_view(), name="products_in_stock"),
    path("api/products/byOrder", views.ProductsByOrderView.as_view(), name="products_by_order"),
    path("api/products/outOfStock", views.ProductsOutOfStockView.as_view(), name="products_out_of_stock"),
    path("api/products/brand/<int:pk>", views.ProductsListByBrand.as_view(), name="product_list_by_brand"),
    path("api/products/subfamily/<int:pk>", views.ProductsListBySubFamily.as_view(), name="product_list_by_subFamily"),

    path("api/category/<int:pk>", views.CategoriesView.as_view(), name="category_detail"),
    path("api/categories", views.CategoriesView.as_view(), name="categories_list_api"),
    path("api/families", views.FamiliesView.as_view(), name="families_list_api"),
    path("api/subfamilies", views.SubFamiliesView.as_view(), name="subFamilies_list_api"),
    path("api/brands", views.BrandsView.as_view(), name="brands_list_api"),
    path("api/attributes", views.AttributesView.as_view(), name="attributes_list_api"),
]

urlpatterns = format_suffix_patterns(urlpatterns)