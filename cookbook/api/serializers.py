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

class NoteSerializer(ExpanderSerializerMixin,serializers.HyperlinkedModelSerializer):
    self_uri = ResourceUriField(
        view_name='note-detail', 
        read_only=True
    )
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Recipe.objects.all(),
        source='recipe',
        write_only=True,
        required=False
    )
        
    recipe = serializers.StringRelatedField(
        read_only=True
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
            'recipe_id',
            'self_uri'
        )

        
class RecipeIngredientSerializer(ExpanderSerializerMixin,serializers.HyperlinkedModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Ingredient.objects.all(),
        source='ingredient',
        write_only=True,
    )
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Unit.objects.all(),
        source='unit',
        write_only=True,
    )
    unit = UnitSerializer(read_only=True)
    recipe = serializers.StringRelatedField(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset = models.Recipe.objects.all(),
        source='recipe',
        write_only=True,
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
            'recipe_id',
            'ingredient_id',
            'unit_id',
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
        # This function allows steps, notes, and recipeingredients
        # to be created at the same time as the recipe.  They should
        # never be created without a recipe.
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
        item_types = ['steps', 'notes', 'recipeingredients']
        item_models = {
            'steps' : models.Step,
            'notes' : models.Note,
            'recipeingredients' : models.RecipeIngredient
        }
        import pdb; pdb.set_trace()
        item_data = {}
        for item_type in item_types:
            if item_type in validated_data.keys():
                item_data[item_type] = validated_data.pop(item_type)
        # if 'steps' in validated_data.keys():
            # steps_data = validated_data.pop('steps')
        # if 'notes' in validated_data.keys():
            # notes_data = validated_data.pop('notes')
        # if 'recipeingredients' in validated_data.keys():
            # recipeingredients_data = validated_data.pop('recipeingredients')
        new_recipe = models.Recipe.objects.create(**validated_data)
        # loop through steps, notes, and recipeingredients
        for item_type in item_types:
            # loop through each individual item in each type
            for item in item_data[item_type]:
                new_item = item_models[item_type].objects.create(
                    recipe=new_recipe,
                    **item
                )
        # for step in steps_data:
            # new_step = models.Step.objects.create(recipe=new_recipe, **step)
        # for note in notes_data:
            # new_note = models.Note.objects.create(recipe=new_recipe, **note)
        
        # for recipeingredient in recipeingredients_data:
            #import pdb; pdb.set_trace()        
            #new_rec_ing = models.RecipeIngredient.objects.create(recipe=new_recipe, **recipeingredient)
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