from rest_framework import serializers
from api.models import Department, Ingredient, Unit
from api.models import Step, Note, Recipe, RecipeIngredient


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'ingredients')

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'department')

class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name', 'name_plural')
        
class StepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Step
        fields = ('id', 'order', 'name', 'recipe')

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'name', 'created', 'recipe')  

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'created', 'steps', 'notes', 'recipeingredients', 'url')
        
class RecipeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'created', 'steps', 'notes', 'recipeingredients', 'url')

class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'qty', 'unit', 'ingredient', 'preparation', 'recipe')