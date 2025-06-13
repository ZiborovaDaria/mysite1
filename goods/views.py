from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.template import context

from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.urls import reverse

from goods.models import Categories, Country, Manufacturer, Products, SubCategories
from goods.utils import q_search

def catalog(request, category_slug=None, subcategory_slug=None):
    goods = Products.objects.all()
    query = request.GET.get('q', '').strip()
    
    # Получаем все категории для фильтра
    categories = Categories.objects.all()
    
    # Определяем текущую категорию и подкатегорию
    category = None
    subcategory = None

    # Фильтрация по подкатегории
    if subcategory_slug:
        subcategory = get_object_or_404(SubCategories, slug=subcategory_slug)
        goods = goods.filter(subcategory=subcategory)
        category = subcategory.category
    
    # Фильтрация по категории
    elif category_slug:
        if category_slug == 'all':
            # Явный запрос на показ всех товаров
            pass
        else:
            category = get_object_or_404(Categories, slug=category_slug)
            goods = goods.filter(category=category)
    
    # Поиск (если есть запрос)
    if query:
        goods = q_search(query)
    
    # Если нет ни категории, ни подкатегории, ни поиска - показываем все товары
    if not category_slug and not subcategory_slug and not query:
        # Можно добавить здесь логику для главной страницы каталога
        pass
    
    # Если запрошена несуществующая категория без поиска
    if not goods.exists() and not query:
        raise Http404("Категория не найдена")


    # Фильтры
    if request.GET.get('on_sale') == 'on':
        goods = goods.filter(discount__gt=0)
    
    if request.GET.get('min_price'):
        goods = goods.filter(price__gte=request.GET['min_price'])
    
    if request.GET.get('max_price'):
        goods = goods.filter(price__lte=request.GET['max_price'])
    
    if request.GET.get('manufacturer'):
        goods = goods.filter(manufacturer_id=request.GET['manufacturer'])
    
    if request.GET.get('country'):
        goods = goods.filter(country_id=request.GET['country'])
    
    # Сортировка
    order_by = request.GET.get('order_by', 'default')
    if order_by == 'price':
        goods = goods.order_by('price')
    elif order_by == '-price':
        goods = goods.order_by('-price')
    elif order_by == '-views':
        goods = goods.order_by('-views')
    
    # Пагинация
    paginator = Paginator(goods, 12)
    page_number = request.GET.get('page')
    goods_page = paginator.get_page(page_number)
    
    context = {
        'goods': goods_page,
        'manufacturers': Manufacturer.objects.all(),
        'countries': Country.objects.all(),
        'categories': categories,
        'category': category,
        'subcategory': subcategory,
        'category_slug': category_slug,
        'subcategory_slug': subcategory_slug,
        'query': query,
    }
    
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    product.views += 1
    product.save()
    
    # Получаем похожие товары из той же категории, исключая текущий товар
    similar_products = Products.objects.filter(
        category=product.category
    ).exclude(id=product.id).order_by('?')[:4]  # 4 случайных товара
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'goods/product.html', context)
