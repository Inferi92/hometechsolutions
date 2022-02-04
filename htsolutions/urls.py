from django.urls import path
from hometechsolutions import settings
from htsolutions import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="HomeTech Solutions API",
      default_version='v2',
      description="Documentação da API da Loja HomeTech Solutions",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   # URLS FRONTEND
   path("", views.index, name="index"),
   path("product/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
   path("products/", views.ProductListView.as_view(), name="products"),
   path("products/brand/<int:pk>", views.productListByBrand, name="products-brand-list"),

   # URLS API ENDPOINTS
   path("api/product/<int:pk>", views.ProductDetailAPI.as_view(), name="single_product_api"),
   path("api/product", views.ProductsListAPI.as_view(), name="products_list_api"),
   path("api/product/inStock", views.ProductsInStockAPI.as_view(), name="products_in_stock_api"),
   path("api/product/byOrder", views.ProductsByOrderAPI.as_view(), name="products_by_order_api"),
   path("api/product/outOfStock", views.ProductsOutOfStockAPI.as_view(), name="products_out_of_stock_api"),
   path("api/product/brand/<int:pk>", views.ProductsListByBrandAPI.as_view(), name="product_list_by_brand_api"),
   path("api/product/subfamily/<int:pk>", views.ProductsListBySubFamilyAPI.as_view(), name="product_list_by_subFamily_api"),
   path("api/category/<int:pk>", views.CategoryDetailAPI.as_view(), name="category_detail_api"),
   path("api/category", views.CategoriesAPI.as_view(), name="categories_list_api"),
   path("api/family/<int:pk>", views.FamilyDetailAPI.as_view(), name="family_detail_api"),
   path("api/family", views.FamiliesAPI.as_view(), name="families_list_api"),
   path("api/subfamily/<int:pk>", views.SubFamilyDetailAPI.as_view(), name="subfamily_detail_api"),
   path("api/subfamily", views.SubFamiliesAPI.as_view(), name="subFamilies_list_api"),
   path("api/brand/<int:pk>", views.BrandDetailAPI.as_view(), name="brand_detail_api"),
   path("api/brand", views.BrandsAPI.as_view(), name="brands_list_api"),
   path("api/attribute/<int:pk>", views.AttributeDetailAPI.as_view(), name="attribute_detail_api"),
   path("api/attribute", views.AttributesAPI.as_view(), name="attributes_list_api"),
   path("api/color/<int:pk>", views.ColorDetailAPI.as_view(), name="color_detail_api"),
   path("api/color", views.ColorsAPI.as_view(), name="Colors_list_api"),

   path("api/docs", schema_view.with_ui('swagger', cache_timeout=0)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)