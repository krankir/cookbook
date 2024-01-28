from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    """Таблица продукта."""

    name = models.CharField(max_length=255)
    count_cooked = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('count_cooked',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField('Название рецепта', max_length=250)
    products = models.ManyToManyField(Product,
                                      related_name='recipes',
                                      through='ProductInRecipe',
                                      verbose_name='Ингридиенты',
                                      )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class ProductInRecipe(models.Model):
    """Промежуточная модель продукта и его количества в рецепте."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               )
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Ингредиент',
                                )
    weight = models.PositiveSmallIntegerField(
        'Количество',
        default=1,
        validators=[MinValueValidator(1, message='Минимальное количество 1 грамм')]
    )

    class Meta:
        verbose_name = 'Ингридиент для рецепта'
        verbose_name_plural = 'Ингридиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'product'],
                name='unique_product'
            )
        ]

    def __str__(self):
        return f'В рецепте "{self.recipe.name}" ингредиента {self.product.name}: {self.weight}-грамм'
