# Generated by Django 4.2 on 2023-04-19 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neorecipe_api', '0003_recipe_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipebook',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]