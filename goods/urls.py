from django.urls import path

from goods import views

app_name='goods'

urlpatterns = [
    path('', views.catalog, name='index'),  # Все товары
    path('search/', views.catalog, name='search'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path('<slug:category_slug>/', views.catalog, name='catalog'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.catalog, name='subcategory'),
]