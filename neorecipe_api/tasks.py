from celery import shared_task
from .models import *

# @shared_task
# def recalculate_recommended_recipes(user):
#    user.recommended_recipes = Recipe.objects.all()[:5]