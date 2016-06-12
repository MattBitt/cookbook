from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField
from api import models
from expander import ExpanderSerializerMixin
import logging
log = logging.getLogger(__name__)


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
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

        
class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='department-detail', 
        read_only=True
    )
    #ingredients = IngredientSerializer(
    #    many=True,
    #    read_only=True
    #)

    class Meta:
        model = models.Department
        fields = (
            'id', 
            'name', 
            'ingredients',
            'self_uri'
        )
        
class UnitSerializer(serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='unit-detail', 
        read_only=True
    )
    
    class Meta:
        model = models.Unit
        fields = (
            'id', 
            'name', 
            'name_plural',
            'self_uri'
        )
        
class StepSerializer(serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='step-detail', 
        read_only=True
    )
    recipe = serializers.StringRelatedField(
        read_only=True
    )
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Recipe.objects.all(),
        source='recipe',
        write_only=True,
        required=False
    )

    class Meta:
        model = models.Step
        fields = (
            'id', 
            'order', 
            'name',
            'recipe',
            'recipe_id',
            'self_uri'
        )            

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='note-detail', 
        read_only=True
    )
    recipe = serializers.StringRelatedField(
        read_only=True
    )
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Recipe.objects.all(),
        source='recipe',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = models.Note
        fields = (
            'id', 
            'name', 
            'created',
            'recipe',
            'recipe_id',
            'self_uri'
        )
        
class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='recipeingredient-detail', 
        read_only=True
    )
    ingredient = IngredientSerializer(
        read_only=True
    )
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Ingredient.objects.all(),
        source='ingredient',
        write_only=True,
    )
    unit = UnitSerializer(
        read_only=True
    )
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Unit.objects.all(),
        source='unit',
        write_only=True,
    )
    recipe = serializers.StringRelatedField(
        read_only=True
    )
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Recipe.objects.all(),
        source='recipe',
        write_only=True,
        required=False
    )

    class Meta:
        model = models.RecipeIngredient
        fields = (
            'id', 
            'qty', 
            'unit', 
            'preparation', 
            'ingredient',
            'recipe',
            'recipe_id',
            'ingredient_id',
            'unit_id',
            'self_uri'
        )
      
class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='recipe-detail', 
        read_only=True
    )
    steps = StepSerializer(
        many=True,
        read_only=False,
        required=True
    )
    notes = NoteSerializer(
        many=True,
        read_only=False
    )
    recipeingredients = RecipeIngredientSerializer(
        many=True,
        read_only=False,
        required=True
    )
    
    def create(self, validated_data):
        # This function allows steps, notes, and recipeingredients
        # to be created at the same time as the recipe.
        # 
        # example input
        # {
        # "name":"boudin",
        # "steps":
            # [{"order":1,"name":"boil meat"}],
        # "notes":
            # [{"name":"not as good as champagnes"}],
        # "recipeingredients":
            # [{"qty":1,"preparation":"chopped","unit_id":1,"ingredient_id":1},
            # {"qty":4,"preparation":"sliced","unit_id":1,"ingredient_id":2}],
        # "url":""}
        log.debug('In Recipe custom create function')
        item_types = ['steps', 'notes', 'recipeingredients']
        item_models = {
            'steps' : models.Step,
            'notes' : models.Note,
            'recipeingredients' : models.RecipeIngredient
        }
        item_data = {}
        for item_type in item_types:
            if item_type in validated_data.keys():
                item_data[item_type] = validated_data.pop(item_type)
        new_recipe = models.Recipe.objects.create(**validated_data)

        # loop through steps, notes, and recipeingredients
        for item_type in item_types:
            # loop through each individual item in each type
            for item in item_data[item_type]:
                new_item = item_models[item_type].objects.create(
                    recipe=new_recipe,
                    **item
                )
        return new_recipe

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