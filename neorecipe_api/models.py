from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class NeorecipeUser(AbstractUser):
    def __str__(self):
        return self.username

class FoodStore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512)

class Ingredient(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    average_price = models.DecimalField(max_digits=6, decimal_places=2)
    source = models.ForeignKey(FoodStore, on_delete=models.SET_NULL, null=True)

class Writer(models.Model):
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)

class RecipeBook(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=128, unique=True)
    publisher = models.CharField(max_length=255, null=True)
    publication_date = models.DateField(null=True)
    authors = models.ManyToManyField(Writer, through='BookContributor')

class BookContributor(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)

class RecipeBookSection(models.Model):
    title = models.CharField(max_length=255)
    book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE)

class Recipe(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    page = models.PositiveIntegerField()
    serves = models.PositiveSmallIntegerField(null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    description = models.CharField(max_length=512)
    source = models.ForeignKey(RecipeBook, on_delete=models.CASCADE, null=True)
    book_section = models.ForeignKey(RecipeBookSection, on_delete=models.CASCADE, null=True)
    estimated_total_price = models.DecimalField(max_digits=6, decimal_places=2)

class Article(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE)
    contents = models.TextField()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    amount_unit = models.CharField(max_length=128)

class RecipeNote(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    note_contents = models.CharField(max_length=1024)

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=512)
