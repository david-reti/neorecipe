# Generated by Django 4.1.5 on 2023-04-03 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neorecipe_api', '0003_alter_recipe_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]