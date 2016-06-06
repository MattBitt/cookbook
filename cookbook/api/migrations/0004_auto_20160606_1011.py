# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-06 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20160606_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('qty', models.IntegerField()),
                ('preparation', models.CharField(max_length=100)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredients', to='api.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredients', to='api.Recipe')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredients', to='api.Unit')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='note',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='step',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
