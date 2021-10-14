from django.contrib import admin
from .models import SiteConfig, Category, Tag, Product

# Register your models here.
@admin.register(SiteConfig)
class SiteConfigModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass