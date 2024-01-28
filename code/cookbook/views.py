from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from cookbook.models import Recipe, Product, ProductInRecipe


def add_product_to_recipe(request):
    """
    Функция добавляет к указанному рецепту указанный продукт с указанным весом.
    Если в рецепте уже есть такой продукт, то функция должна поменять его вес
    в этом рецепте на указанный.
    """
    recipe_id = int(request.GET.get('recipe_id'))
    product_id = int(request.GET.get('product_id'))
    weight = int(request.GET.get('weight'))

    recipe = Recipe.objects.get(pk=recipe_id)
    product = Product.objects.get(pk=product_id)

    recipe_product, created = ProductInRecipe.objects.get_or_create(
        recipe=recipe, product=product)

    if not created:
        recipe_product.weight += weight
        recipe_product.save()

    return JsonResponse({'success': 'Продукт успешно добавлен в рецепт.'})


def cook_recipe(request):
    """
    Функция увеличивает на единицу количество приготовленных блюд для каждого
    продукта, входящего в указанный рецепт.
    """
    recipe_id = int(request.GET.get('recipe_id'))
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    products_in_recipe = recipe.productinrecipe_set.select_related('product')
    for recipe_product in products_in_recipe:
        recipe_product.product.count_cooked += 1
    updated_products = [recipe_product.product for recipe_product in
                        products_in_recipe]
    Product.objects.bulk_update(updated_products, ['count_cooked'])
    return JsonResponse({'success': 'счётчик увеличен'})


def show_recipes_without_product(request):
    """
    Функция возвращает HTML страницу, на которой размещена таблица. В таблице
    отображены id и названия всех рецептов, в которых указанный продукт
    отсутствует, или присутствует в количестве меньше 10 грамм.
    """
    product_id = int(request.GET.get('product_id'))
    recipes_without_product = Recipe.objects.filter(
        ~Q(productinrecipe__product=product_id) | Q(
            productinrecipe__product=product_id,
            productinrecipe__weight__gt=10)
    ).prefetch_related(
        Prefetch('products', Product.objects.filter(id=product_id),
                 'product_in_get')).distinct()
    product = [product for recipe in recipes_without_product for product in recipe.product_in_get][0]

    context = {
        'recipes': recipes_without_product,
        'product': product
    }
    return render(request, 'cookbook/show_recipes.html', context)
