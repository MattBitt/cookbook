from django.test import TestCase, Client
from api import models
import json

class DepartmentTestCase(TestCase):
    fixtures = ['api.json']

    def setUp(self):
        self.client = Client()

    def testGetAllDepartments(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def testGetOneDepartments(self):
        response = self.client.get('/api/departments/2/')
        self.assertEqual(response.status_code, 200)
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

    def testDeleteDepartment(self):
        response = self.client.delete('/api/departments/2/')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/api/departments/2/')
        self.assertEqual(response.status_code, 404)

        