from rest_framework.serializers import *
from .models import *
from django.contrib.auth.models import User

class FoodStoreSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = FoodStore
        fields = ['user', 'slug', 'name', 'address']

class WriterSerializer(ModelSerializer):
    class Meta:
        model = Writer
        fields = ['first_name', 'last_name', 'full_name']

class RecipeBookSectionSerializer(ModelSerializer):
    book = PrimaryKeyRelatedField(queryset=RecipeBook.objects.all())
    class Meta:
        model = RecipeBookSection
        fields = ['title', 'book']

class IngredientSerializer(ModelSerializer):
    source = PrimaryKeyRelatedField(queryset=FoodStore.objects.all(), write_only=True)
    class Meta:
        model = Ingredient
        fields = ['slug', 'name', 'description', 'average_price', 'source']

class RecipeIngredientSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'ingredient', 'amount', 'amount_unit']

class RecipeNoteSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    class Meta:
        model = RecipeNote
        fields = ['recipe', 'note_contents']

class RecipeStepSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    class Meta:
        model = RecipeStep
        fields = ['recipe', 'step_number', 'description']

class RecipeSerializer(ModelSerializer):
    source = PrimaryKeyRelatedField(queryset=RecipeBook.objects.all())
    book_section = PrimaryKeyRelatedField(queryset=RecipeBookSection.objects.all())
    ingredients = IngredientSerializer(many=True)
    steps = RecipeStepSerializer(many=True)
    notes = RecipeNoteSerializer(many=True)

    def validate(self, data):
        if not data.get('source', None) and not data.get('book_section', None):
            raise ValidationError('Either the book or book section needs to be provided for the recipe.')

    class Meta:
        model = Recipe
        fields = ['slug', 'title', 'page', 'serves', 'steps', 'notes', 'ingredients', 'description', 'source', 'book_section', 'estimated_total_price']

class RecipeBookSerializer(ModelSerializer):
    authors = StringRelatedField(many=True, read_only=True)
    class Meta:
        model = RecipeBook
        fields = ['slug', 'title', 'isbn', 'publisher', 'publication_date', 'authors']