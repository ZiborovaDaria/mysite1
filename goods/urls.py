from django.urls import path

from goods import views

app_name='goods'

urlpatterns = [
    path('search/', views.catalog, name='search'),
    # path('', views.catalog, {'category_slug': 'all'}, name='index'),
    path('<slug:category_slug>/', views.catalog, name='catalog'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.catalog, name='subcategory'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]