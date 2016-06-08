from django.shortcuts import render
from rest_framework import viewsets
from api import models
from api import serializers
from api.request_logging import mixins

import logging
log = logging.getLogger(__name__)



# example of querying accross relationships
# this query gives all recipes that have the ingredient milk in them
# models.Recipe.objects.filter(recipeingredients__ingredient__name='milk')

class DepartmentViewSet(viewsets.ModelViewSet, mixins.RequestLogViewMixin):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    log.debug('DepartmentView logging WORKS!')
    
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    log.debug('In ingredient viewset function')
    #def initial(self):
        #log.debug('In ingredient initial function')
        #super(IngredientViewSet, self).initial(request, *args, **kwargs)

class UnitViewSet(viewsets.ModelViewSet):
    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer
    
class NoteViewSet(viewsets.ModelViewSet):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteSerializer
    
class StepViewSet(viewsets.ModelViewSet):
    queryset = models.Step.objects.all()
    serializer_class = serializers.StepSerializer
    
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    log.debug('RecipeView logging WORKS!')
    
class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = models.RecipeIngredient.objects.all()
    serializer_class = serializers.RecipeIngredientSerializer