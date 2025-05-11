from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories

def index(request):

    categories=Categories.objects.all()

    context = {
        'title': 'ЕМЕХ-авто - Главная',
        'content': 'Магазин атвозапчастей ЕМЕХ',
        'categories': categories
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'ЕМЕХ-авто - О нас',
        'content': 'Дополнительная информация',
        'text_on_page' : "text"
    }

    return render(request, 'main/about.html', context)
