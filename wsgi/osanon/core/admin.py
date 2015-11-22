from django.contrib import admin
from core.models import Center

# Register your models here.

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'street', 'town', 'lat', 'lng')
    search_fields = ['name']
