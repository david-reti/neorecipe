from rest_framework import generics, mixins, filters
from .serializers import *
from .permissions import *

class FoodStoresView(generics.ListCreateAPIView):
    serializer_class = FoodStoreSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'name', 'address' ]
    ordering = [ 'name' ]
    permission_classes = [ OnlyStaffCanCreate ]

    def get_queryset(self):
        return FoodStore.objects.filter(user = self.request.user)

class SingleFoodStoreView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodStoreSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]

    def get_queryset(self):
        return FoodStore.objects.filter(user = self.request.user)

class WritersView(generics.ListCreateAPIView):
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = ['first_name', 'last_name', 'full_name']
    ordering = [ 'last_name', 'first_name' ]
    permission_classes = [ OnlyStaffCanCreate ]

class SingleWriterView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]

class IngredientsView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'name', 'average_price' ]
    ordering = [ 'name' ]
    permission_classes = [ OnlyStaffCanCreate ]

class SingleIngredientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]

class RecipeStepsView(generics.ListCreateAPIView):
    serializer_class = RecipeStepSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering = [ 'step_number' ]
    permission_classes = [ OnlyStaffCanCreate ]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('recipe', None)).steps.all()

class SingleRecipeStepView(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = RecipeStepSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('recipe', None)).steps.all()

class RecipeIngredientsView(generics.ListCreateAPIView):
    serializer_class = RecipeIngredientSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = ['ingredient__name', 'amount']
    ordering = [ 'ingredient__name' ]
    permission_classes = [ OnlyStaffCanCreate ]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('recipe', None)).ingredients.all()

class SingleRecipeIngredientView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeIngredientSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('recipe', None)).ingredients.all()

class RecipesView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'title', 'page', 'serves', 'estimated_total_price' ]
    ordering = [ 'title' ]
    permission_classes = [ OnlyStaffCanCreate ]

    def get_queryset(self):
        if 'source' in self.kwargs.keys():
            return Recipe.objects.filter(book__id = self.kwargs.get('souce', 1))
        else:
            return Recipe.objects.filter(section__id = self.kwargs.get('book_section', 1))

class SingleRecipeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeBook.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]

class RecipeBooksView(generics.ListCreateAPIView):
    queryset = RecipeBook.objects.all()
    serializer_class = RecipeBookSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'slug', 'title', 'publisher', 'publication_date' ]
    ordering = [ 'title' ]
    permission_classes = [ OnlyStaffCanCreate ]

class SingleRecipeBookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeBook.objects.all()
    serializer_class = RecipeBookSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]

class RecommendedRecipesView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'title', 'page', 'serves', 'estimated_total_price' ]
    ordering = [ 'title' ]

    def get_queryset(self):
        return Recipe.objects.all()