from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from charity.models import *
from account.models import *
from django.contrib.auth.models import User
import json


class CharityTestCase(TestCase):

    def setUp(self):
        Charity.objects.create(
            name="testing1",
            description="helping children",
            register_id=124,
            paypal="paypal1")
        Charity.objects.create(
            name="testing2",
            description="helping elderly",
            register_id=125,
            paypal="paypal2")

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


class CharityCreationTests(APITestCase):

    def setUp(self):
        self.charity = {'name': 'foo', 'register_id': 1, 'type': 'E',
                        'description': 'Some info', 'target': 'C',
                        'paypal': 'foo@bar.com', 'charitableActivity': 10,
                        'fundraising': 10, 'admin': 80}

    def testCharityCreateSerializer(self):
        response = self.client.post('/api/charity/register',
                                    {'account': {'username': 'ming', 'password': '123'},
                                     'description': 'for testing',
                                     'paypal': 'test paypal'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.charity['username'] = 'ming'
        self.charity['password'] = '123'
        response = self.client.post(
            '/api/charities', self.charity, format='json')
 
        charity = Charity.objects.get(register_id=1)
        self.assertEqual(charity.admin, 80)
        print("Charity creation passed.")


class CharityUpdateTest(APITestCase):

    def setUp(self):
        self.charity = {'name': 'foo', 'register_id': 2, 'type': 'E',
                        'description': 'Some info', 'target': 'C',
                        'paypal': 'foo@bar.com'}

    def testCharityUpdateSerializer(self):
        response = self.client.post('/api/charity/register',
                                    {'account': {'username': 'ming', 'password': '123'},
                                     'description': 'for testing',
                                     'paypal': 'test paypal'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.charity['username'] = 'ming'
        self.charity['password'] = '123'
        response = self.client.post(
            '/api/charities', self.charity, format='json')
        account = User.objects.get(username='ming')
        self.assertEqual(CharityAccount.objects.get(
            account=account).charity.paypal, 'foo@bar.com')
        update = {'username': 'ming', 'paypal': 'changed'}
        response = self.client.patch(
            '/api/update_charity', update, format='json')
        self.assertEqual(CharityAccount.objects.get(
            account=account).charity.paypal, 'changed')
        print("Charity update passed.")


class VolunteeringUpdateTestCase(APITestCase):

    def setUp(self):
        self.charity = {'name': 'foo', 'register_id': 1, 'type': 'E',
                                'description': 'Some info', 'target': 'C',
                                'paypal': 'foo@bar.com'}
        self.client.post('/api/charity/register',
                         {'account': {'username': 'ming', 'password': '123'},
                          'description': 'for testing',
                          'paypal': 'test paypal'}, format='json')
        self.charity['username'] = 'ming'
        self.charity['password'] = '123'
        self.client.post('/api/charities', self.charity, format='json')
        self.volunteering = {'name': 'test', 'charity': 1, 'description': 'testing', 'start_date': '2017-01-01', 'end_date': '2018-01-01',
                             'url': 'www.example.com'}
        response = self.client.post(
            '/api/volunteering', self.volunteering, format='json')

    def testUpdateVolunteering(self):
        response = self.client.patch(
            '/api/volunteering/1', {'name': 'changed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/volunteering/1')
        response_data = json.loads(response.content.decode())
        self.assertEqual(response_data['name'], 'changed')
        print("Updating volunteering passed")

    def testDeleteVolunteering(self):
        response = self.client.delete('/api/volunteering/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/volunteering')
        response_data = json.loads(response.content.decode())
        self.assertEqual(len(response_data), 0)
        print("Deleting volunteering passed")


class CharitySearchTestCase(APITestCase):

    def setUp(self):
        charity = {'username': 'ming', 'id': 1, 'name': 'foo', 'register_id': 1, 'type': 'E',
                   'description': 'Some info', 'target': 'C',
                   'total_income': 10000, 'paypal': 'foo@bar.com',
                   'charitableActivity': 0, 'fundraising': 0, 'admin': 0}
        account = {'username': 'ming', 'password': '123',
                   'description': 'cccc', 'paypal': 'testing'}
        charity1 = {'username': 'ming1', 'id': 2, 'name': 'bar', 'register_id': 2, 'type': 'D',
                    'description': 'Some info1', 'target': 'C',
                    'total_income': 1000000, 'paypal': 'foo1@bar.com',
                   'charitableActivity': 0, 'fundraising': 0, 'admin': 0}
        account1 = {'username': 'ming1', 'password': '123',
                    'description': 'cccc', 'paypal': 'testing'}
        charity2 = {'username': 'ming2', 'id': 3, 'name': 'baz', 'register_id': 3, 'type': 'E',
                    'description': 'Some info2', 'target': 'E',
                    'total_income': 9999, 'paypal': 'foo2@bar.com',
                    'charitableActivity': 0, 'fundraising': 0, 'admin': 0}
        account2 = {'username': 'ming2', 'password': '123',
                    'description': 'cccc', 'paypal': 'testing'}
        charity3 = {'username': 'ming3', 'id': 4, 'name': 'foo', 'register_id': 4, 'type': 'AN',
                    'description': 'Some info3', 'target': 'E',
                    'total_income': 1000000000, 'paypal': 'foo3@bar.com',
                    'charitableActivity': 0, 'fundraising': 0, 'admin': 0}
        account3 = {'username': 'ming3', 'password': '123',
                    'description': 'cccc', 'paypal': 'testing'}
        charity4 = {'username': 'ming4', 'id': 5, 'name': 'boo', 'register_id': 5, 'type': 'E',
                    'description': 'Some info4', 'target': 'D',
                    'total_income': 123456, 'paypal': 'foo4@bar.com',
                    'charitableActivity': 0, 'fundraising': 0, 'admin': 0}
        account4 = {'username': 'ming4', 'password': '123',
                    'description': 'cccc', 'paypal': 'testing'}
        self.charities = [charity, charity1, charity2, charity3, charity4]
        self.accounts = [account, account1, account2, account3, account4]
        for i in range(0, 5):
            try:
                self.client.post('/api/charity/register',
                                 self.accounts[i], format='json')
                self.client.post('/api/charities',
                                 self.charities[i], format='json')
                self.charities[i].pop('username')
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
        response = self.client.get(
            '/api/charities/?type=E&target=D&min_income=123456')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEquals(len(response_data), 1)
        self.assertIn(self.charities[4], response_data)
        print("Searching by multiple params passed")
