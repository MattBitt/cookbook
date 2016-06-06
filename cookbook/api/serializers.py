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
    ingredient = IngredientSerializer()
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
            'preparation', 
            'recipe', 
            'ingredient', 
            'self_uri'
        )
    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient')
        existing_ing = models.Ingredient.objects.filter(name=ingredient_data['name']).first()
        if existing_ing is None:
            ing = models.Ingredient.objects.create(**ingredient_data)
        else:
            ing = existing_ing
        
        rec_ing = models.RecipeIngredient.objects.create(ingredient=ing, **validated_data)
        return rec_ing
        
class RecipeSerializer(serializers.ModelSerializer):
    self_uri = ResourceUriField(
        view_name='recipe-detail', 
        read_only=True
    )
    steps = StepSerializer(
        many=True,
        read_only=False,
        required=False
    )
    notes = NoteSerializer(
        many=True,
        read_only=True
    )
    recipeingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True
    )
    
    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        new_recipe = models.Recipe.objects.create(**validated_data)
        import pdb; pdb.set_trace()
        for step in steps_data:
            #shouldn't have to do the next step
            # need to figure out how to make recipe not required for
            # a new step
            recipe_data = step.pop('recipe')
            new_step = models.Step.objects.create(recipe=new_recipe, **step)
        return recipe
    
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