from django.urls import path
from .views import *

urlpatterns = [
    path('food-stores', FoodStoresView.as_view()),
    path('food-stores/<int:pk>', SingleFoodStoreView.as_view()),
    path('writers', WritersView.as_view()),
    path('writers/<int:pk>', SingleWriterView.as_view()),
    path('ingredients', IngredientsView.as_view()),
    path('ingredients/<int:pk>', SingleIngredientView.as_view()),
    path('recipes/<slug:source>', RecipesView.as_view()),
    path('recipes/<slug:source>/<slug:section>', RecipesView.as_view()),
    path('recipes/<int:pk>', SingleRecipeView.as_view()),
    path('recipes/<int:recipe>/steps', RecipeStepsView.as_view()),
    path('recipes/<int:recipe>/steps/<int:pk>', SingleRecipeStepView.as_view()),
    path('recipes/<int:recipe>/ingredients', RecipeIngredientsView.as_view()),
    path('recipes/<int:recipe>/ingredients/<int:pk>', SingleRecipeIngredientView.as_view()),
    path('recipe-books', RecipeBooksView.as_view()),
    path('recipe-books/<int:pk>', SingleRecipeBookView.as_view()),
]