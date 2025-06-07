from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template import context

from goods.models import Categories, Country, Manufacturer, Products, SubCategories
from goods.utils import q_search

def catalog(request, category_slug=None, subcategory_slug=None):
    goods = Products.objects.all()
    
    # Получаем все категории для фильтра
    categories = Categories.objects.all()
    
    # Определяем текущую категорию и подкатегорию
    category = None
    subcategory = None

    # Фильтрация по категории/подкатегории
    if category_slug == 'all':
        pass
    elif subcategory_slug:
        subcategory = get_object_or_404(SubCategories, slug=subcategory_slug)
        goods = goods.filter(category=subcategory.category)
        category_slug = subcategory.category.slug
    elif category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        goods = goods.filter(category=category)
    
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
    }
    
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):

    product=Products.objects.get(slug=product_slug)

    context = {
        'product': product
        }
    return render(request, 'goods/product.html',context)