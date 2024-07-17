from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.models import Category, Product


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    exclude = 'slug',

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = 'slug',
