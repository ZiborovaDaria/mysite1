from django.contrib import admin

from main.models import Contact, Promotion, Store

# Register your models here.
admin.site.register(Promotion)
# admin.site.register(Store)
admin.site.register(Contact)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'phone', 'is_main')
    list_filter = ('city', 'is_main')
    search_fields = ('address', 'phone', 'email')
    list_editable = ('is_main',)
    fieldsets = (
        (None, {
            'fields': ('city', 'address', 'is_main')
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'opening_hours')
        }),
        ('Координаты', {
            'fields': ('latitude', 'longitude')
        }),
    )