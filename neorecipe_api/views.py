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

class ContributorsView(generics.ListCreateAPIView):
    queryset = BookContributor.objects.all()
    serializer_class = ContributorSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = ['name', 'role']
    ordering = [ 'name' ]
    permission_classes = [ OnlyStaffCanCreate ]

class SingleContributorView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookContributor.objects.all()
    serializer_class = ContributorSerializer
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
        books = Recipe.objects.all()
        if 'title' in self.request.GET:
            books = books.filter(title__icontains = self.request.GET['title'])
        if 'category' in self.request.GET:
            books = books.filter(category__in = self.request.GET['category'].split(','))
        if 'source' in self.request.GET:
            books = books.filter(book__id = self.request.GET['source'])
        if 'book_section' in self.request.GET:
            books = books.filter(section__id = self.request.GET['book_section'])
        return books

class SingleRecipeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]
    lookup_field = 'slug'

    def get_queryset(self):
        if 'slug' in self.request.GET:
            return Recipe.objects.filter(slug = self.request.GET['slug'])
        return Recipe.objects.all()

class RecipeBooksView(generics.ListCreateAPIView):
    serializer_class = RecipeBookSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'slug', 'title', 'publisher', 'publication_date' ]
    ordering = [ 'title' ]
    permission_classes = [ OnlyStaffCanCreate ]

    def get_queryset(self):
        books = RecipeBook.objects.all()
        if 'title' in self.request.GET:
            books = books.filter(title__icontains = self.request.GET['title'])
        if 'category' in self.request.GET:
            books = books.filter(category__iexact = self.request.GET['category'])
        return books

class SingleRecipeBookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeBook.objects.all()
    serializer_class = RecipeBookSerializer
    permission_classes = [ OnlyStaffCanUpdate, OnlyStaffCanDelete ]
    lookup_field = 'slug'

class RecommendedRecipesView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'title', 'page', 'serves', 'estimated_total_price' ]
    ordering = [ 'title' ]

    def get_queryset(self):
        return Recipe.objects.all()