from django.test import TestCase, Client
from api import models
import json

class RecipeTestCase(TestCase):
    fixtures = ['api.json']

    def setUp(self):
        self.client = Client()
    
    def testGetRecipe(self):
        response = self.client.get('/api/recipes/4/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'new recipe number 3')


        
        
    #def testGetIngredientNameFromRecipe(self):
    #    response = self.client.get('/api/recipes/4/')
    #    self.assertEqual(
    #        response.data['recipeingredients'][0]['ingredient']['name'],
    #        'broccoli'
    #    )