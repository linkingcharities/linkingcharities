from django.test import TestCase
from payment.models import *
from charity.models import *
from django.utils import timezone, dateparse
from django.contrib.auth.models import User
from account.models import (
  DonorAccount,
  CharityAccount
)
import json

# Create your tests here.

class PaymentTestCase(TestCase):

    def setUp(self):
        self.time = timezone.now()
        user = User.objects.create(username='ming', password="ming")
        DonorAccount.objects.create(account=user)
        Payment.objects.create(username='ming'
                         , account_id = 1
                         , charity='charilink@gmail.com'
                         , charity_id = 1
                         , currency='USD'
                         , amount='1'
                         , date=self.time)
        self.charity = Charity.objects.create(name = 'foo', register_id = 1, 
                   type = 'E',
                   description = 'Some info', target = 'C',
                   paypal = 'foo@bar.com')
        return

    def testGetPaymentAPIWithUser(self):
        
        response = self.client.get('/api/show_payment'
                                  , { 'username' : 'ming', 'payment': '1' }
                                  , format='json')
        
        returnData = json.loads(response.content.decode())
        self.assertEquals(len(returnData),1)
        entry = returnData[0]
        self.assertEquals(entry['username'], 'ming')
        self.assertEquals(entry['charity'], 'charilink@gmail.com')
        self.assertEquals(entry['currency'], 'USD')
        self.assertEquals(entry['amount'], 1)
        self.assertEquals(dateparse.parse_datetime(entry['date']), self.time)
        
        print("Get payment API passed.")

    def testGetPaymentAPICanGetMultiplePayments(self):
        
        Payment.objects.create(username='ming'
                         , charity='someothercharity@gmail.com'
                         , currency='USD'
                         , amount='23'
                         , date=timezone.now())
        
        response = self.client.get('/api/show_payment'
                                   , { 'username': 'ming' }
                                   , format='json')
        returnData = json.loads(response.content.decode())
        self.assertEquals(len(returnData),2)

        print("Get payment API multiple payments passed.")

    def testMakePaymentAPICanProduceRecord(self):
        user = User.objects.create(username="make_payment", password = "ming")
        data = { 'item_name': 'make_payment'
               , 'account_id': user.id
               , 'business': 'foo@bar.com'
               , 'charity_id': self.charity.id
               , 'mc_currency': 'USD'
               , 'payment_gross': '12' }
        
        request = self.client.post('/api/make_payment', data, format='json')
        
        checkRequest = self.client.get('/api/show_payment'
                                      , {'username': 'make_payment'}
                                      , format='json')
        returnData = json.loads(checkRequest.content.decode())
        self.assertEquals(len(returnData), 1)
        entry = returnData[0]
        self.assertEquals(entry['charity'], 'foo')
        self.assertEquals(entry['currency'], 'USD')
        self.assertEquals(entry['amount'], 12)
        self.assertEquals(entry['account_id'], user.id)

        print("Make payment API passed.")
