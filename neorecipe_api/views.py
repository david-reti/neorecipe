from rest_framework import generics, mixins, filters
from rest_framework.response import Response
from .serializers import *
from .permissions import *
from django.db.models import Q
from django.core.mail import send_mail

class FoodStoresView(generics.ListCreateAPIView):
    serializer_class = FoodStoreSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'name', 'address' ]
    ordering = [ 'name' ]
    permission_classes = [ AnyoneCanView, AnyoneCanCreate ]

    def get_queryset(self):
        return FoodStore.objects.filter(user = self.request.user)

class SingleFoodStoreView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodStoreSerializer
    permission_classes = [ AnyoneCanView, AnyoneCanUpdate, AnyoneCanDelete ]

    def get_queryset(self):
        return FoodStore.objects.filter(user = self.request.user)

class ContributorsView(generics.ListCreateAPIView):
    queryset = BookContributor.objects.all()
    serializer_class = ContributorSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = ['name', 'role']
    ordering = [ 'name' ]
    permission_classes = [ AnyoneCanView, AnyoneCanCreate ]

class SingleContributorView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookContributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [ AnyoneCanView, AnyoneCanUpdate, OnlyStaffCanDelete ]

class IngredientsView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'name', 'average_price' ]
    ordering = [ 'name' ]
    permission_classes = [ AnyoneCanView, AnyoneCanCreate ]

    def get_serializer(self, instance=None, data=None, partial=False):
        if data is not None:
            return super(IngredientsView, self).get_serializer(instance=instance, data=data, many=True, partial=partial)
        else:
            return super(IngredientsView, self).get_serializer(instance=instance, many=True, partial=partial)

class SingleIngredientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [ AnyoneCanView, AnyoneCanUpdate, AnyoneCanCreate ]

class RecipeStepsView(generics.ListCreateAPIView):
    serializer_class = RecipeStepSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering = [ 'step_number' ]
    permission_classes = [ AnyoneCanView, AnyoneCanCreate ]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('recipe', None)).steps.all()
    
    def get_serializer(self, instance=None, data=None, partial=False):
        if data is not None:
            return super(IngredientsView, self).get_serializer(instance=instance, data=data, many=True, partial=partial)
        else:
            return super(IngredientsView, self).get_serializer(instance=instance, many=True, partial=partial)

class SingleRecipeStepView(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = RecipeStepSerializer
    permission_classes = [ AnyoneCanCreate, AnyoneCanDelete ]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('slug', None)).steps.all()

class RecipeIngredientsView(generics.ListCreateAPIView):
    serializer_class = RecipeIngredientSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = ['ingredient__name', 'amount']
    ordering = [ 'ingredient__name' ]
    permission_classes = [ AnyoneCanView, AnyoneCanCreate ]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('recipe', None)).ingredients.all()
    
    def get_serializer(self, instance=None, data=None, partial=False):
        if data is not None:
            return super(IngredientsView, self).get_serializer(instance=instance, data=data, many=True, partial=partial)
        else:
            return super(IngredientsView, self).get_serializer(instance=instance, many=True, partial=partial)

class SingleRecipeIngredientView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeIngredientSerializer
    permission_classes = [ AnyoneCanView, AnyoneCanUpdate, AnyoneCanDelete]

    def get_queryset(self):
        return Recipe.objects.get(self.kwargs.get('slug', None)).ingredients.all()

class RecipesView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'title', 'page', 'serves', 'estimated_total_price' ]
    ordering = [ 'title' ]
    permission_classes = [ AnyoneCanView, AnyoneCanCreate ]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            recipes = Recipe.objects.filter(Q(source__publicly_accessible = True))
        elif self.request.user.is_staff:
            recipes = Recipe.objects.all()
        else:    
            recipes = Recipe.objects.filter(Q(source__publicly_accessible = True) | Q(source__creator = self.request.user))

        if 'title' in self.request.GET:
            recipes = recipes.filter(title__icontains = self.request.GET['title'])
        if 'category' in self.request.GET:
            recipes = recipes.filter(category__in = self.request.GET['category'].split(','))
        if 'source' in self.request.GET:
            recipes = recipes.filter(book__id = self.request.GET['source'])
        if 'book_section' in self.request.GET:
            recipes = recipes.filter(section__id = self.request.GET['book_section'])
        return recipes
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class SingleRecipeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [ AnyoneCanView, OwnerAndStaffCanUpdate, OwnerAndStaffCanDelete ]
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Recipe.objects.all()
        if 'slug' in self.request.GET:
            return Recipe.objects.filter(Q(slug = self.request.GET['slug']), Q(source__publicly_accessible = True) | Q(source__creator = self.request.user))
        return Recipe.objects.filter(Q(source__publicly_accessible = True) | Q(source__creator = self.request.user))

    def get(self, request, *args, **kwargs):
        serializer = RecipeSerializer(self.get_queryset().get(slug = kwargs['slug']))
        to_return = serializer.data.copy()
        to_return['user_can_edit'] = request.user.pk == serializer.data.get('creator') or request.user.is_staff
        return Response(to_return)

class RecipeBooksView(generics.ListCreateAPIView):
    serializer_class = RecipeBookSerializer
    filter_backends = [ filters.OrderingFilter ]
    ordering_fields = [ 'slug', 'title', 'publisher', 'publication_date' ]
    ordering = [ 'title' ]
    permission_classes = [ AnyoneCanView, AnyoneCanCreate ]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            books = RecipeBook.objects.filter(Q(publicly_accessible = True) & Q(approved = True))
        elif self.request.user.is_staff:
            books = RecipeBook.objects.all()
        else:    
            books = RecipeBook.objects.filter(Q(Q(publicly_accessible = True) & Q(approved = True)) | Q(creator = self.request.user))

        if 'title' in self.request.GET:
            books = books.filter(title__icontains = self.request.GET['title'])
        if 'category' in self.request.GET:
            books = books.filter(category__iexact = self.request.GET['category'])
        return books

    def perform_create(self, serializer):
        if serializer.validated_data.get('publicly_accessible', False) == True:
            staff = NeorecipeUser.objects.get(is_staff = True)
            send_mail(f"Approve Recipe Book: {serializer.validated_data.get('slug', 'ERROR: BOOK NOT PROVIDED')}", 
                      f"Please take a look and approve the recipe book with slug: {serializer.validated_data.get('slug', '')}",
                      "infra@neorecipe.app",
                      [ staff.email ])

        serializer.save(creator=self.request.user)

class SingleRecipeBookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeBook.objects.all()
    serializer_class = RecipeBookSerializer
    permission_classes = [ OwnerAndStaffCanUpdate, OwnerAndStaffCanDelete ]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        serializer = RecipeBookSerializer(self.get_queryset().get(slug = kwargs['slug']))
        to_return = serializer.data.copy()
        to_return['user_can_edit'] = request.user.is_staff or request.user.pk == serializer.data.get('creator')
        return Response(to_return)

class UserPrefsView(generics.RetrieveUpdateAPIView):
    queryset = NeorecipeUser.objects.all()
    permission_classes = [ OnlyCurrentUserAndStaffCanView, OnlyCurrentUserAndStaffCanUpdate ]
    serializer_class = UserPrefsSerializer

# class RecommendedRecipesView(generics.ListAPIView):
#     serializer_class = RecipeSerializer
#     filter_backends = [ filters.OrderingFilter ]
#     ordering_fields = [ 'title', 'page', 'serves', 'estimated_total_price' ]
#     ordering = [ 'title' ]

#     def get_queryset(self):
#         return Recipe.objects.all()
