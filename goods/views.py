from django.shortcuts import render
from django.template import context

import goods
from goods.models import Products

def catalog(request):

    goods=Products.objects.all()

    context = {
        'title': 'Home - Каталог',
        'goods': goods,
        }
    return render(request, 'goods/catalog.html', context)

def product(request):
    return render(request, 'goods/product.html')