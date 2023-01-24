from .models import NeorecipeUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class NeorecipeUserCreationForm(UserCreationForm):
    class Meta:
        model = NeorecipeUser
        fields = ['username', 'email']

class NeorecipeUserChangeForm(UserChangeForm):
    class Meta:
        model = NeorecipeUser
        fields = ['username', 'email']