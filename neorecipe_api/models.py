from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class FoodStore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True)

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    average_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    source = models.ForeignKey(FoodStore, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeBook(models.Model):
    slug = models.SlugField(unique=True)
    isbn = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=255)
    style = models.CharField(max_length=512, blank=True)
    creator = models.ForeignKey('NeorecipeUser', on_delete=models.PROTECT)
    category = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, null = True, blank=True)
    description = models.TextField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    publicly_accessible = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}{' (' + self.publisher + ')' if self.publisher else ''}" 

class BookContributor(models.Model):
    book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE, related_name='contributors')
    name = models.CharField(max_length=255, default='')
    role = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class RecipeBookSection(models.Model):
    title = models.CharField(max_length=255)
    chapter = models.IntegerField(null=True, blank=True)
    book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=256)
    page = models.PositiveIntegerField(null=True, blank=True)
    serves = models.PositiveSmallIntegerField(null=True, blank=True)
    creator = models.ForeignKey('NeorecipeUser', on_delete=models.PROTECT)
    contributor = models.ForeignKey(BookContributor, on_delete=models.PROTECT, null=True, blank=True)
    category = models.CharField(max_length=256, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    description = models.TextField(blank=True, null=True)
    preparation_time = models.TimeField(blank=True, null=True)
    style = models.CharField(max_length=512, blank=True)
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
    recipe = models.ForeignKey(Recipe, default=0, on_delete=models.CASCADE)
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
    description = models.CharField(max_length=4096)

    def __str__(self):
        return f"Step {self.step_number + 1} - {self.recipe}"

class RecommendedRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey('NeorecipeUser', on_delete=models.CASCADE)
    strength = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Recommendation: {self.recipe} for {self.user}"

class PantryItem(models.Model):
    user = models.ForeignKey('NeorecipeUser', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    amount_unit = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f"{self.ingredient} in {self.user}'s pantry"

class NeorecipeUser(AbstractUser):
    recommended_recipes = models.ManyToManyField(Recipe)
    userprefs = models.TextField(default='')

    def __str__(self):
        return self.username
