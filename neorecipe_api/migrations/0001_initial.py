# Generated by Django 4.1.5 on 2023-01-12 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('average_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='neorecipe_api.foodstore')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('page', models.PositiveIntegerField()),
                ('serves', models.PositiveSmallIntegerField(null=True)),
                ('description', models.CharField(max_length=512)),
                ('estimated_total_price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('isbn', models.DecimalField(decimal_places=0, max_digits=13, unique=True)),
                ('publisher', models.CharField(max_length=255, null=True)),
                ('publication_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.PositiveSmallIntegerField()),
                ('description', models.CharField(max_length=512)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neorecipe_api.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_contents', models.CharField(max_length=1024)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neorecipe_api.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('amount_unit', models.CharField(max_length=128)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neorecipe_api.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neorecipe_api.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeBookSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neorecipe_api.recipebook')),
            ],
        ),
        migrations.AddField(
            model_name='recipebook',
            name='authors',
            field=models.ManyToManyField(to='neorecipe_api.writer'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='book_section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neorecipe_api.recipebooksection'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='neorecipe_api.RecipeIngredient', to='neorecipe_api.ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neorecipe_api.recipebook'),
        ),
    ]
