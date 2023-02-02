from django.contrib import admin
from .models import *
from .forms import NeorecipeUserCreationForm, NeorecipeUserChangeForm
from django.contrib.auth.admin import UserAdmin

class NeorecipeUserAdmin(UserAdmin):
    add_form = NeorecipeUserCreationForm
    form = NeorecipeUserChangeForm
    model = NeorecipeUser
    list_display = ['email', 'username']

admin.site.register(RecipeBook)
admin.site.register(RecipeBookSection)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeStep)
admin.site.register(BookContributor)
admin.site.register(NeorecipeUser, NeorecipeUserAdmin)
