from __future__ import unicode_literals

from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=25, blank=False)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<Department {} {}>'.format(self.id, self.name)
        
class Ingredient(models.Model):
    name = models.CharField(max_length=50, blank=False)
    department = models.ForeignKey(
        Department, 
        related_name='ingredients', 
        on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<Ingredient {} {}>'.format(self.id, self.name)
        
class Unit(models.Model):
    name = models.CharField(max_length=25, blank=False)
    name_plural = models.CharField(max_length=25, blank=True)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<Unit {} {}>'.format(self.id, self.name)

class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=25, blank=False)
    image_path = models.CharField(max_length=150, blank=True)
    url = models.CharField(max_length=200, blank=True)
    
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<Recipe {} {}>'.format(self.id, self.name)
        
        
class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=False)
    recipe = models.ForeignKey(
        Recipe, 
        related_name='notes',
        on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<Note {} {}>'.format(self.id, self.name) 

class Step(models.Model):
    name = models.CharField(max_length=200, blank=False)
    order = models.IntegerField(blank=False)
    recipe = models.ForeignKey(
        Recipe, 
        related_name='steps',
        on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<Step {} {}>'.format(self.id, self.name)         

class RecipeIngredient(models.Model):
    qty = models.IntegerField()
    preparation = models.CharField(max_length=100)
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipeingredients',
        on_delete=models.CASCADE
    )
    unit = models.ForeignKey(
        Unit,
        related_name='recipeingredients',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, 
        related_name='recipeingredients',
        on_delete=models.CASCADE
    )
        
    def __str__(self):
        return '{} {} {}, {}'.format(self.qty, self.unit, self.ingredient, self.preparation)
    
    def __unicode__(self):
        return '{} {} {}, {}'.format(self.qty, self.unit, self.ingredient, self.preparation)
    
    def __repr__(self):
        return '<RecipeIngredient {}>'.format(self.id) 