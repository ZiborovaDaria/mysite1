from django.contrib import admin

from goods.models import Categories, Country, Manufacturer,Products, SubCategories

admin.site.register(Manufacturer)
admin.site.register(Country)

@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','quantity','price','discount']
    list_editable=['discount',]
    search_fields=['name','description']
    list_filter=['quantity','category','discount']
    fields=['name','category','slug','description','image','quantity',('price','discount'),]