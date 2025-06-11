from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.urls import reverse

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        # db_table='Manufacturer'
        verbose_name= "Производителя"
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        # db_table='Country'
        verbose_name= "Страну"
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table='category'
        verbose_name= "Категорию"
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    

class SubCategories(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название подкатегории')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    category = models.ForeignKey(to=Categories, on_delete=models.PROTECT, related_name='subcategories', verbose_name='Категория')
    
    class Meta:
        db_table = 'subcategory'
        verbose_name = "Подкатегорию"
        verbose_name_plural = 'Подкатегории'
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description=models.TextField(blank=True, null=True, verbose_name='ОписаниеL')
    image = models.ImageField(upload_to='gooods_images',blank=True, null=True, verbose_name='Изображение')
    price=models.DecimalField(default=0.00,max_digits=7,decimal_places=2, verbose_name='Цена')
    discount=models.DecimalField(default=0.00,max_digits=4,decimal_places=2, verbose_name='Скидка в %')
    quantity=models.PositiveIntegerField(default=0, verbose_name='Количество')
    category=models.ForeignKey(to=Categories, on_delete=models.PROTECT,verbose_name= "Категория")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)  # для сортировки по популярности
    subcategory = models.ForeignKey(SubCategories, on_delete=models.SET_NULL, null=True,blank=True,verbose_name='Подкатегория')

    class Meta:
        db_table='product'
        verbose_name= "Продукт"
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    

    def display_id(self):
        return f'{self.id:05}'
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100,2)
        
        return self.price

