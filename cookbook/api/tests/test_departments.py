from django.test import TestCase
from api import models
from django.test import Client
import json

class DepartmentTestCase(TestCase):
    fixtures = ['api.json']

    def setUp(self):
        # Test definitions as before.
        self.client = Client()

    def testGetAllDepartments(self):
        response = self.client.get('/api/departments/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.data), 3)

    def testGetOneDepartments(self):
        response = self.client.get('/api/departments/2/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains 5 customers.
        self.assertEqual(response.data['name'], 'produce')
        
    def testCreateDepartment(self):
        data = {'name' : 'hba'}
        data_string = json.dumps(data)
        response = self.client.post(
            '/api/departments/', 
            content_type='application/json',
            data=data_string
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['id'], 5)
        
class RecipeTestCase(TestCase):
    fixtures = ['api.json']

    def setUp(self):
        # Test definitions as before.
        self.client = Client()
    
    def testGetRecipe(self):
        response = self.client.get('/api/recipes/4/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['recipeingredients'][0]['ingredient']['name'],
            'broccoli'
        )
        