from django.http import HttpResponse
from django.shortcuts import render


def index(request):


    context = {
        'title': 'ЕМЕХ-авто - Главная',
        'content': 'Магазин автозапчастей ЕМЕХ'
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'ЕМЕХ-авто - О нас',
        'content': 'Дополнительная информация',
        'text_on_page' : "text"
    }

    return render(request, 'main/about.html', context)
