from rest_framework.serializers import *
from .models import *

class FoodStoreSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=NeorecipeUser.objects.all())
    class Meta:
        model = FoodStore
        fields = ['user', 'slug', 'name', 'address']

class ContributorSerializer(ModelSerializer):
    class Meta:
        model = BookContributor
        fields = ['name', 'role']

class RecipeBookSectionSerializer(ModelSerializer):
    book = PrimaryKeyRelatedField(queryset=RecipeBook.objects.all())
    class Meta:
        model = RecipeBookSection
        fields = ['title']

class IngredientSerializer(ModelSerializer):
    source = PrimaryKeyRelatedField(queryset=FoodStore.objects.all(), write_only=True)
    class Meta:
        model = Ingredient
        fields = ['slug', 'name', 'description', 'average_price', 'source']

class RecipeIngredientSerializer(ModelSerializer):
    ingredient = IngredientSerializer()
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'amount_unit', 'preparation']

class RecipeNoteSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    class Meta:
        model = RecipeNote
        fields = ['recipe', 'note_contents']

class RecipeStepSerializer(ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['step_number', 'description']

class RecipeSerializer(ModelSerializer):
    source = StringRelatedField()
    book_section = PrimaryKeyRelatedField(queryset=RecipeBookSection.objects.all())
    ingredients = RecipeIngredientSerializer(many=True, source="recipeingredient_set")
    steps = RecipeStepSerializer(many=True, source="recipestep_set")
    notes = RecipeNoteSerializer(many=True, source="recipenote_set")

    def validate(self, data):
        if not data.get('source', None) and not data.get('book_section', None):
            raise ValidationError('Either the book or book section needs to be provided for the recipe.')

    class Meta:
        model = Recipe
        fields = ['slug', 'title', 'category', 'page', 'serves', 'steps', 'style', 'preparation_time', 'notes', 'ingredients', 'description', 'source', 'book_section', 'estimated_total_price']

class RecipeBookSerializer(ModelSerializer):
    contributors = StringRelatedField(many=True, read_only=True, source="bookcontributor_set")
    sections = StringRelatedField(many=True, source="recipebooksection_set")
    class Meta:
        model = RecipeBook
        fields = ['slug', 'title', 'description', 'sections', 'isbn', 'publicly_accessible', 'category', 'style', 'publisher', 'publication_date', 'contributors']