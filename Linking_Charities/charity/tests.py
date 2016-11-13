from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from charity.models import *
import json

class CharityTestCase(TestCase):

    def setUp(self):
        Charity.objects.create(
            name="testing1",
            description="helping children",
            register_id = 124)
        Charity.objects.create(
            name="testing2",
            description="helping elderly",
            register_id = 125)

    def testGetAllCharity(self):
        queryset = Charity.objects.all()
        try:
            c1 = Charity.objects.get(name="testing1")
        except Exception:
            self.fail("Charity \"testing1\" could not be created.")
        try:
            c2 = Charity.objects.get(name="testing2")
        except Exception:
            self.fail("Charity \"testing2\" could not be created.")
        self.assertEqual(len(queryset), 2)
        print("Get all Charity passed.")

class CharitySearchTestCase(APITestCase):

    def setUp(self):
        charity = {'id': 1, 'name': 'foo', 'register_id': 1, 'type': 'E',
                   'description': 'Some info', 'target': 'C',
                   'total_income': 10000, 'paypal': 'foo@bar.com'}
        charity1 = {'id': 2, 'name': 'bar', 'register_id': 2, 'type': 'D',
                   'description': 'Some info1', 'target': 'C',
                   'total_income': 1000000, 'paypal': 'foo1@bar.com'}
        charity2 = {'id': 3, 'name': 'baz', 'register_id': 3, 'type': 'E',
                   'description': 'Some info2', 'target': 'E',
                   'total_income': 9999, 'paypal': 'foo2@bar.com'}
        charity3 = {'id': 4, 'name': 'foo', 'register_id': 4, 'type': 'AN',
                   'description': 'Some info3', 'target': 'E',
                   'total_income': 1000000000 , 'paypal': 'foo3@bar.com'}
        charity4 = {'id': 5, 'name': 'boo', 'register_id': 5, 'type': 'E',
                   'description': 'Some info4', 'target': 'D',
                   'total_income': 123456, 'paypal': 'foo4@bar.com'}
        self.charities = [charity, charity1, charity2, charity3, charity4]
        for charity in self.charities:
            try:
                self.client.post('/api/charities', charity, format='json')
            except Exception:
                self.fail('Error in post request for' + str(charity['name']))

    def testSearchByID(self):
        response = self.client.get('/api/charities/?id=5')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 1)
        self.assertEquals(response_data[0]['id'], 5)
        print("Searching by id passed")

    def testSearchByName(self):
        response = self.client.get('/api/charities/?name=foo')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 2)
        self.assertIn(self.charities[0], response_data)
        self.assertIn(self.charities[3], response_data)
        print("Searching by name passed")

    def testSearchByType(self):
        response = self.client.get('/api/charities/?type=E')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 3)
        self.assertIn(self.charities[0], response_data)
        self.assertIn(self.charities[2], response_data)
        self.assertIn(self.charities[4], response_data)
        print("Searching by type passed")

    def testSearchByTarget(self):
        response = self.client.get('/api/charities/?target=E')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 2)
        self.assertIn(self.charities[2], response_data)
        self.assertIn(self.charities[3], response_data)
        print("Searching by target passed")

    def testSearchByMinIncome(self):
        response = self.client.get('/api/charities/?min_income=10000')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 4)
        self.assertIn(self.charities[0], response_data)
        self.assertIn(self.charities[1], response_data)
        self.assertIn(self.charities[3], response_data)
        self.assertIn(self.charities[4], response_data)
        print("Searching by minimum income passed")

    def testSearchByMaxIncome(self):
        response = self.client.get('/api/charities/?max_income=123455')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 2)
        self.assertIn(self.charities[0], response_data)
        self.assertIn(self.charities[2], response_data)
        print("Searching by maximum income passed")

    def testSearchByMinAndMaxIncome(self):
        min_income = 10000
        max_income = 123456
        response = self.client.get('/api/charities/?' + 'min_income='
                                   + str(min_income) + '&max_income='
                                   + str(max_income))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 2)
        self.assertIn(self.charities[0], response_data)
        self.assertIn(self.charities[4], response_data)
        print("Searching by minimum income and maximum income passed")

    def testSearchByMultipleParams(self):
        response = self.client.get('/api/charities/?type=E&target=D&min_income=123456')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 1)
        self.assertIn(self.charities[4], response_data)
        print("Searching by multiple params passed")
