from django.contrib import admin

from cookbook.models import Product, Recipe, ProductInRecipe


class RecipeProductInline(admin.TabularInline):
    model = ProductInRecipe
    extra = 1


@admin.register(Product)
class CategoriesAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class CategoriesAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]

