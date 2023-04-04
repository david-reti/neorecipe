from rest_framework.serializers import *
from .models import *
from django.db import transaction

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
    # source = PrimaryKeyRelatedField(queryset=FoodStore.objects.all(), required=False)
    class Meta:
        model = Ingredient
        fields = ['slug', 'name', 'description', 'average_price']

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
    source_slug = SlugField(write_only=True, allow_null=True)
    book_section = PrimaryKeyRelatedField(queryset=RecipeBookSection.objects.all(), required=False)
    ingredients = RecipeIngredientSerializer(many=True, source="recipeingredient_set")
    steps = RecipeStepSerializer(many=True, source="recipestep_set")
    notes = RecipeNoteSerializer(many=True, source="recipenote_set", required=False)

    # def validate(self, data):
    #     if not data.get('source', None) and not data.get('book_section', None):
    #         raise ValidationError('Either the book or book section needs to be provided for the recipe.')

    @transaction.atomic()
    def create(self, validated_data):
        steps = validated_data.pop('recipestep_set')
        ingredients = validated_data.pop('recipeingredient_set')

        recipe = Recipe.objects.create(**validated_data)

        if validated_data.get('source_slug', None):
            recipe.source = RecipeBook.objects.get(slug=validated_data.pop('source_slug'))
        else:
            recipe.source = None

        for step in steps:
            RecipeStep.objects.create(recipe=recipe, **step)
        for recipe_ingredient in ingredients:
            ingredient_data = recipe_ingredient.pop('ingredient')
            ingredient = Ingredient.objects.create(**ingredient_data)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, **recipe_ingredient)
        
        return recipe
    
    @transaction.atomic()
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        steps = validated_data.pop('recipestep_set')
        ingredients = validated_data.pop('recipeingredient_set')

        if validated_data.get('source_slug', None):
            instance.source = RecipeBook.objects.get(slug=validated_data.pop('source_slug'))
        else:
            instance.source = None

        step_list = []
        for step in steps:
            step, _ = RecipeStep.objects.get_or_create(recipe=instance, **step)
            step_list.append(step)

        for step in set([step.description for step in instance.recipestep_set.all()]) - set([step.description for step in step_list]):
            RecipeStep.objects.get(recipe=instance, description=step).delete()

        ingredient_list = []
        ingredient_slugs = [ingredient['ingredient']['slug'] for ingredient in ingredients]
        for recipe_ingredient in ingredients:
            ingredient_data = recipe_ingredient.pop('ingredient')
            new_ingredient, _ = Ingredient.objects.get_or_create(**ingredient_data)
            new_recipe_ingredient, _ = RecipeIngredient.objects.get_or_create(recipe=instance, ingredient=new_ingredient, **recipe_ingredient)
            ingredient_list.append(new_recipe_ingredient)

        for ingredient_to_remove in set([ingredient.ingredient.slug for ingredient in instance.recipeingredient_set.all()]) - set(ingredient_slugs):
            RecipeIngredient.objects.get(ingredient__slug=ingredient_to_remove).delete()

        instance.steps = step_list
        instance.recipeingredient_set.set(ingredient_list, clear=True)
        instance.save()

        return instance

    class Meta:
        model = Recipe
        fields = ['slug', 'title', 'category', 'page', 'serves', 'steps', 'style', 'preparation_time', 'notes', 'ingredients', 'description', 'source', 'source_slug', 'book_section', 'estimated_total_price']

class RecipeBookSerializer(ModelSerializer):
    contributors = StringRelatedField(many=True, read_only=True, source="bookcontributor_set")
    sections = StringRelatedField(many=True, source="recipebooksection_set")
    class Meta:
        model = RecipeBook
        fields = ['slug', 'title', 'description', 'sections', 'isbn', 'publicly_accessible', 'category', 'style', 'publisher', 'publication_date', 'contributors']