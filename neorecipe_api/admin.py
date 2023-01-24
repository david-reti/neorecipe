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
admin.site.register(NeorecipeUser, NeorecipeUserAdmin)
