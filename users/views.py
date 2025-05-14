from django.shortcuts import render

def login(request):

    context = {
        'title': 'ЕМЕХ-авто - Авторизация',
        'content': 'Магазин автозапчастей ЕМЕХ'
    }
    return render(request, 'users/login.html', context)

def registration(request):

    context = {
        'title': 'ЕМЕХ-авто - Регистрация',
        'content': 'Магазин автозапчастей ЕМЕХ'
    }
    return render(request, 'users/registration.html', context)

def profile(request):

    context = {
        'title': 'ЕМЕХ-авто - Кабинет',
        'content': 'Магазин автозапчастей ЕМЕХ'
    }
    return render(request, 'users/profile.html', context)

def logout(request):

    context = {
        'title': 'ЕМЕХ-авто - Главная',
        'content': 'Магазин автозапчастей ЕМЕХ'
    }
    return render(request, '', context)
