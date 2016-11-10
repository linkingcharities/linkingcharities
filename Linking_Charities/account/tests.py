from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from account.models import *

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
