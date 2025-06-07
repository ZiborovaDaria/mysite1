from django.contrib import admin

from main.models import Contact, Promotion, Store

# Register your models here.
admin.site.register(Promotion)
admin.site.register(Store)
admin.site.register(Contact)