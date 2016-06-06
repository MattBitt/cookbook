from django.shortcuts import render
from rest_framework import viewsets
from api import models
from api import serializers


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

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
    
class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = models.RecipeIngredient.objects.all()
    serializer_class = serializers.RecipeIngredientSerializer