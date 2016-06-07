from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField
from api import models
from expander import ExpanderSerializerMixin



class IngredientSerializer(ExpanderSerializerMixin, serializers.HyperlinkedModelSerializer):
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

        
class DepartmentSerializer(ExpanderSerializerMixin, serializers.HyperlinkedModelSerializer):
    #ingredients = IngredientSerializer(
    #    many=True,
    ##    read_only=True
    #)
    self_uri = ResourceUriField(view_name='department-detail', read_only=True)
    class Meta:
        model = models.Department
        fields = (
            'id', 
            'name', 
            'ingredients',
            'self_uri'
        )
        expandable_fields = {
        'ingredients' : (IngredientSerializer, (), {'many' : True})}
    #def get_validation_exclusions(self):
    #    exclusions = super(DepartmentSerializer, self).get_validation_exclusions()
    #    return exclusions + ['ingredients']
        
class UnitSerializer(ExpanderSerializerMixin,serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(view_name='unit-detail', read_only=True)
    class Meta:
        model = models.Unit
        fields = (
            'id', 
            'name', 
            'name_plural',
            'self_uri'
        )
        
class StepSerializer(ExpanderSerializerMixin,serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='step-detail', 
        read_only=True
    )
    recipe = serializers.StringRelatedField(
        many=False,
        read_only=False,
        required=False
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

class NoteSerializer(ExpanderSerializerMixin,serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='note-detail', 
        read_only=True
    )
    recipe = serializers.StringRelatedField(
        many=False,
        read_only=False,
        required=False
    )
    
    def get_validation_exclusions(self):
        exclusions = super(NoteSerializer, self).get_validation_exclusions()
        return exclusions + ['recipe']
        
    class Meta:
        model = models.Note
        fields = (
            'id', 
            'name', 
            'created',
            'recipe',
            'self_uri'
        )

        
class RecipeIngredientSerializer(ExpanderSerializerMixin,serializers.HyperlinkedModelSerializer):
    ingredient = serializers.StringRelatedField(
        many=False,
        read_only=False,
        required=False
    )    
    unit = serializers.StringRelatedField(
        many=False,
        read_only=False,
        required=False
    )
    recipe = serializers.StringRelatedField(
        many=False,
        read_only=False,
        required=False
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
            'preparation', 
            'ingredient',
            'recipe',
            'self_uri'
        )
        
        
    def get_validation_exclusions(self):
        exclusions = super(RecipeIngredientSerializer, self).get_validation_exclusions()
        return exclusions + ['ingredient', 'unit', 'recipe']
        
class RecipeSerializer(ExpanderSerializerMixin,serializers.HyperlinkedModelSerializer):
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
        read_only=False,
        required=False
    )
    recipeingredients = RecipeIngredientSerializer(
        many=True,
        read_only=False,
        partial=True,
        required=False
    )
    
    def create(self, validated_data):
        #import pdb; pdb.set_trace()
        if 'steps' in validated_data.keys():
            steps_data = validated_data.pop('steps')
        if 'notes' in validated_data.keys():
            notes_data = validated_data.pop('notes')
        if 'recipeingredients' in validated_data.keys():
            recipeingredients_data = validated_data.pop('recipeingredients')
        new_recipe = models.Recipe.objects.create(**validated_data)
        for step in steps_data:
            new_step = models.Step.objects.create(recipe=new_recipe, **step)
        for note in notes_data:
            new_note = models.Note.objects.create(recipe=new_recipe, **note)
        for recipeingredient in self.context['request'].data['recipeingredients']:
            #import pdb; pdb.set_trace()
            ingredient_name = recipeingredient.pop('ingredient')
            ing, created = models.Ingredient.objects.get_or_create(
                name=ingredient_name)
            #existing_ing = models.Ingredient.objects.filter(name=ingredient_name).first()
            #if existing_ing is None:
            #    ing = models.Ingredient.objects.create(**recipeingredient['ingredient'])
            #else:
            #    ing = existing_ing
            unit_name = recipeingredient.pop('unit')
            unit, created = models.Unit.objects.get_or_create(
                name=unit_name)
            rec_ing = models.RecipeIngredient.objects.create(
                ingredient=ing, 
                recipe=new_recipe, 
                unit=unit,
                **recipeingredient)
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

        #expandable_fields = {
        #    'steps' : (StepSerializer, (), {'many' : True, 'read_only' : False}),
        #    'notes' : (NoteSerializer, (), {'many' : True, 'read_only' : False}),
        #    'recipeingredients' : (
        #        RecipeIngredientSerializer, 
        #        (), 
        #        {'many' : True, 'read_only' : False}
        #    )
        #}
        
        def get_validation_exclusions(self):
            exclusions = super(RecipeSerializer, self).get_validation_exclusions()
            return exclusions + ['recipeingredients', 'steps', 'notes']        