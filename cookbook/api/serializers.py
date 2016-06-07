from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField
from api import models




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
    ingredients = IngredientSerializer(
        many=True,
        read_only=True
    )
    self_uri = ResourceUriField(view_name='department-detail', read_only=True)
    class Meta:
        model = models.Department
        fields = (
            'id', 
            'name', 
            'ingredients',
            'self_uri'
        )
    def get_validation_exclusions(self):
        exclusions = super(DepartmentSerializer, self).get_validation_exclusions()
        return exclusions + ['ingredients']
        
class UnitSerializer(serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(view_name='unit-detail', read_only=True)
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

    class Meta:
        model = models.Step
        fields = (
            'id', 
            'order', 
            'name', 
            'recipe',
            'self_uri'
        )            

class NoteSerializer(serializers.HyperlinkedModelSerializer):
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

        
class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    #ingredient = IngredientSerializer(
    #    many=False,
    #    read_only=True
    #)
    ingredient = serializers.SlugRelatedField(
        queryset=models.Ingredient.objects.all(), 
        slug_field='name'
    )
    #ingredient = serializers.StringRelatedField(
    #    many=False
    #)
    self_uri = ResourceUriField(
        view_name='recipeingredient-detail', 
        read_only=True
    )
    def get_validation_exclusions(self):
        exclusions = super(DepartmentSerializer, self).get_validation_exclusions()
        return exclusions + ['ingredients']

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
    #def create(self, validated_data):
    #    ingredient_data = validated_data.pop('ingredient')
    #    existing_ing = models.Ingredient.objects.filter(name=ingredient_data['name']).first()
    ##    if existing_ing is None:
    #        ing = models.Ingredient.objects.create(**ingredient_data)
    #    else:
    #        ing = existing_ing
    #    
    #    rec_ing = models.RecipeIngredient.objects.create(ingredient=ing, **validated_data)
    #    return rec_ing
        
class RecipeSerializer(serializers.HyperlinkedModelSerializer):
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
    
    #def create(self, validated_data):
    #    steps_data = validated_data.pop('steps')
    #    new_recipe = models.Recipe.objects.create(**validated_data)
    #    import pdb; pdb.set_trace()
    #    for step in steps_data:
    #        #shouldn't have to do the next step
            # need to figure out how to make recipe not required for
            # a new step
    #        recipe_data = step.pop('recipe')
    #        new_step = models.Step.objects.create(recipe=new_recipe, **step)
    #    return recipe
    
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