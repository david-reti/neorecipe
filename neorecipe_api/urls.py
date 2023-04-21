from django.urls import path
from .views import *

urlpatterns = [
    #path('food-stores', FoodStoresView.as_view()),
    #path('food-stores/<int:pk>', SingleFoodStoreView.as_view()),
    #path('contributors', ContributorsView.as_view()),
    #path('contributors/<int:pk>', SingleContributorView.as_view()),
    path('ingredients', IngredientsView.as_view()),
    #path('ingredients/<int:pk>', SingleIngredientView.as_view()),
    path('recipes', RecipesView.as_view()),
    path('recipes/<slug:slug>', SingleRecipeView.as_view()),
    path('recipes/<slug:slug>/ingredients', SingleRecipeIngredientView.as_view()),
    path('recipes/<slug:slug>/steps', SingleRecipeStepView.as_view()),
    path('recipe-books', RecipeBooksView.as_view()),
    path('recipe-books/<slug:slug>', SingleRecipeBookView.as_view()),
    path('users/<int:pk>/preferences', UserPrefsView.as_view()),
    path('users/<int:pk>/pantry', UserPantryView.as_view()),
    path('users/<int:pk>/recommended-recipes', RecommendedRecipesView.as_view()),
]
