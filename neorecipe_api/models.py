from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class FoodStore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True)

class Ingredient(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    average_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    source = models.ForeignKey(FoodStore, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Writer(models.Model):
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

class RecipeBook(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=128, unique=True)
    publisher = models.CharField(max_length=255, null = True, blank=True)
    publication_date = models.DateField(null = True, blank=True)
    authors = models.ManyToManyField(Writer, through='BookContributor')

    def __str__(self):
        return f"{self.title} ({self.publisher})" 

class BookContributor(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)

class RecipeBookSection(models.Model):
    title = models.CharField(max_length=255)
    chapter = models.IntegerField(null=True, blank=True)
    book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.book}"

class Recipe(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    page = models.PositiveIntegerField(null=True, blank=True)
    serves = models.PositiveSmallIntegerField(null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    description = models.CharField(max_length=512)
    source = models.ForeignKey(RecipeBook, on_delete=models.CASCADE, null=True, blank=True)
    book_section = models.ForeignKey(RecipeBookSection, on_delete=models.CASCADE, null=True, blank=True)
    estimated_total_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

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
    preparation = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f"{self.ingredient} for {self.recipe}"

class RecipeNote(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    note_contents = models.CharField(max_length=1024)

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=512)

class NeorecipeUser(AbstractUser):
    recommended_recipes = models.ManyToManyField(Recipe)
    def __str__(self):
        return self.username