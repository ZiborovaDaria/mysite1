from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Contact, Promotion, Store


def index(request):
    promotions = Promotion.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    context = {
        'title': 'ЕМЕХ-авто - Главная',
        'content': 'Магазин автозапчастей ЕМЕХ',
        'promotions': promotions
    }
    return render(request, 'main/index.html', context)

def about(request):
    stores = Store.objects.order_by('-is_main', 'city')
    contacts = Contact.objects.order_by('order')
    
    contact_types = {
        'PHONE': contacts.filter(contact_type='PHONE'),
        'EMAIL': contacts.filter(contact_type='EMAIL'),
        'ADDRESS': contacts.filter(contact_type='ADDRESS'),
        'SOCIAL': contacts.filter(contact_type='SOCIAL'),
    }

    context = {
        'title': 'ЕМЕХ-авто - О нас',
        'text_on_page': {
            'description': """
                <p>ЕМЕХ-авто - это ведущий поставщик автозапчастей в России с более чем 15-летним опытом работы на рынке.</p>
                <p>Мы предлагаем только оригинальные запчасти и расходные материалы от проверенных производителей.</p>
            """,
            'advantages': [
                "Официальный дилер ведущих производителей",
                "Более 50,000 наименований в каталоге",
                "Гарантия качества на все товары",
                "Быстрая доставка по всей России",
                "Профессиональные консультации"
            ],
            'mission': "Мы стремимся сделать покупку автозапчастей простой, быстрой и выгодной для каждого клиента."
        },
        'stores': stores,
        'contacts': contacts,
        'contact_types': contact_types,
        'meta_description': 'Информация о компании ЕМЕХ-авто - магазины автозапчастей, контакты, акции',
    }
    return render(request, 'main/about.html', context)
