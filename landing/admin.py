from django.contrib import admin

from .models import Category, GalleryItem, Product, SocialLink


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_featured", "is_active", "order")
    list_filter = ("is_featured", "is_active", "category")
    search_fields = ("name", "short_description", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "-created_at")


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("title",)
    ordering = ("order", "-created_at")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "platform", "is_primary_cta", "is_active", "order")
    list_filter = ("platform", "is_primary_cta", "is_active")
    search_fields = ("label", "url")
    ordering = ("order", "platform")
