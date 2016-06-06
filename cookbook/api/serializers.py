from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField
from api import models


class DepartmentSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(view_name='department-detail', read_only=True)
    class Meta:
        model = models.Department
        fields = ('id', 'name', 'ingredients', 'self_uri')

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ('id', 'name', 'department')

class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Unit
        fields = ('id', 'name', 'name_plural')
        
class StepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Step
        fields = ('id', 'order', 'name', 'recipe')

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Note
        fields = ('id', 'name', 'created', 'recipe')  

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Recipe
        fields = ('id', 'name', 'created', 'steps', 'notes', 'recipeingredients', 'url')
        
class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'qty', 'unit', 'ingredient', 'preparation', 'recipe')