from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from account.models import *
import json

# Create your tests here.

class AccountTestCase(TestCase):
    
    def setUp(self):
        user = User.objects.create_user("ming", 
            "test@hotmail.com", 
            "123")
        donor = DonorAccount.objects.create(account=user)
        return

    def testDonorAccountCreation(self):
        try:
            self.assertEqual(User.objects.get(username="ming").email, 
                "test@hotmail.com")
        except Exception:
            self.fail("Error, donor account creation failed.")
        
        print("Donor Account Creation passed.")
 
class SerializerTestCase(APITestCase):

    def setUp(self):
        self.data = {"account": {'username': 'test_serializer', 'password': '1234'} }
     
    def testDonorAccountSerializerCreation(self):
        response = self.client.post('/api/donor/register', self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try:
            User.objects.get(username="test_serializer")
        except Exception:
            self.fail("Error, serializer cannot create Donor Account.")
        print("Donor account serializer passed.")

    def testCharityAccountSerializerCreation(self):
        data = self.data
        data['description'] = 'helping children'
        data['paypal'] = 'charilink@hotmail.com'
        response = self.client.post('/api/charity/register'
                       , data
                       , format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try: 
            user = User.objects.get(username="test_serializer")
            charity = CharityAccount.objects.get(account=user)
            self.assertEquals(charity.description, 'helping children')
            self.assertEquals(charity.paypal, 'charilink@hotmail.com')
        except Exception:
            self.fail("Error, serializer cannot create Charity Account.")
        print("Charity account serializer passed.")

class SerializerAuthenticationTestCase(APITestCase):
     
    def setUp(self):
        self.donorData = { 'account' : { 'username': 'auth_test', 'password': '1234'} }
        self.client.post('/api/donor/register', self.donorData, format='json')
        self.charityData = { 'account' : { 'username': 'auth_charity', 'password': '1234' } }
        self.charityData['description'] = 'auth testing description'
        self.charityData['paypal'] = 'auth testing paypal'
        self.client.post('/api/charity/register', self.charityData, format='json')
         
    def testDonorAccountAuthentication(self):
        donorLoginData = { 'username': 'auth_test', 'password': '1234' }
        response = self.client.post('/api/login', donorLoginData, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        auth_key = json.loads(response.content.decode())['token']
        id = json.loads(response.content.decode())['id']
        user = User.objects.get(username=donorLoginData['username'])
        token = Token.objects.get(user=user)
        self.assertEquals(auth_key, token.key)
        self.assertEquals('1',id)

        print("Donor account authentication passed.")
 
    def testDonorAccountAuthenticationWrongPasswordFails(self):
        donorLoginData = { 'username': 'auth_test', 'password': '111'}
        response = self.client.post('/api/login'
                                    , donorLoginData
                                    , format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST) 
        returnData = json.loads(response.content.decode())['non_field_errors']
        self.assertEqual(returnData[0], 'Incorrect password.')
        
        print("Donor account wrong password authentication passed.")

    def testDonorAccountAuthenticationInvalidUsername(self):
        donorLoginData = { 'username': 'invalid', 'password': '1234' }
        response = self.client.post('/api/login'
                                    , donorLoginData
                                    , format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        returnData = json.loads(response.content.decode())['non_field_errors']
        self.assertEquals(returnData[0], 'Username is not valid.')

        print("Donor account invalid username authentication passed.")

    def testCharityAccountAuthentication(self):
        charityLoginData = { 'username': 'auth_charity', 'password': '1234' }
        response = self.client.post('/api/login', charityLoginData, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        auth_key = json.loads(response.content.decode())['token']
        user = User.objects.get(username=charityLoginData['username'])
        token = Token.objects.get(user=user)
        id = json.loads(response.content.decode())['id']
        self.assertEquals(auth_key, token.key)
        self.assertEquals('2',id)
 
        print("Charity account authentication passed.")  

    def testCharityAccountAuthenticationWrongPasswordFails(self):
        charityLoginData = { 'username': 'auth_charity', 'password': '111'}
        response = self.client.post('/api/login', charityLoginData, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        returnData = json.loads(response.content.decode())['non_field_errors']
        self.assertEqual(returnData[0], 'Incorrect password.')

        print("Charity account wrong password authentication passed.")

    def testCharityAccountAuthenticationInvalidUsername(self):
        charityLoginData = { 'username': 'invalid', 'password': '1234' }
        response = self.client.post('/api/login', charityLoginData, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        returnData = json.loads(response.content.decode())['non_field_errors']
        self.assertEquals(returnData[0], 'Username is not valid.')

        print("Charity account invalid username authentication passed.") 


class GetAccountInfoTestCase(APITestCase):

    def setUp(self):
        self.client.post('/api/donor/register', { 'account': {'username': 'ming', 'password': '123'}}, format='json')
        self.client.get('/api/account_info/?username=ming', format='json')

    def testDonorAccountInfo(self):
        response = self.client.get('/api/account_info/?username=ming', format='json')
        print("Retrieve donor acccount info passed")

    def testCharityAccountInfo(self):
        print("Retrieve charity account info")
