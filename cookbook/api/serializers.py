from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField
from api import models




class IngredientSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(
        view_name='ingredient-detail', 
        read_only=True
    )
    class Meta:
        model = models.Ingredient
        fields = (
            'id', 
            'name', 
            'department', 
            'self_uri'
        )

        
class DepartmentSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(view_name='department-detail', read_only=True)
    ingredients = IngredientSerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = models.Department
        fields = (
            'id', 
            'name', 
            'ingredients', 
            'self_uri'
        )
        
class UnitSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(view_name='unit-detail', read_only=True)
    class Meta:
        model = models.Unit
        fields = (
            'id', 
            'name', 
            'name_plural', 
            'self_uri'
        )
        
class StepSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(
        view_name='step-detail', 
        read_only=True
    )
    class Meta:
        model = models.Step
        fields = (
            'id', 
            'order', 
            'name', 
            'recipe', 
            'self_uri'
        )            

class NoteSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(
        view_name='note-detail', 
        read_only=True
    )
    class Meta:
        model = models.Note
        fields = (
            'id', 
            'name', 
            'created', 
            'recipe', 
            'self_uri'
        )

        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(
        many=False,
        read_only=True
    )
    self_uri = ResourceUriField(
        view_name='recipeingredient-detail', 
        read_only=True
    )
    class Meta:
        model = models.RecipeIngredient
        fields = (
            'id', 
            'qty', 
            'unit', 
            'ingredient', 
            'preparation', 
            'recipe', 
            'self_uri'
        )
        
class RecipeSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(
        view_name='recipe-detail', 
        read_only=True
    )
    steps = StepSerializer(
        many=True,
        read_only=True
    )
    notes = NoteSerializer(
        many=True,
        read_only=True
    )
    recipeingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True
    )
    
    class Meta:
        model = models.Recipe
        fields = (
            'id', 
            'name', 
            'created', 
            'steps', 
            'notes', 
            'recipeingredients', 
            'url', 
            'self_uri'
        )