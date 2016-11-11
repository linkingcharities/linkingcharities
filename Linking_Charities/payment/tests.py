from django.test import TestCase
from payment.models import *
from django.utils import timezone, dateparse
import json

# Create your tests here.

class PaymentTestCase(TestCase):

    def setUp(self):
        self.time = timezone.now()
        Payment.objects.create(username='ming'
                         , charity='charilink@gmail.com'
                         , currency='USD'
                         , amount='1'
                         , date=self.time)
        return

    def testGetPaymentAPIWithUser(self):
        
        response = self.client.get('/api/show_payment'
                                  , { 'username' : 'ming' }
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
        data = { 'username': 'make_payment'
               , 'charity': 'charilink@gmail.com'
               , 'currency': 'USD'
               , 'amount': '12' }
        
        request = self.client.post('/api/make_payment', data, format='json')
        
        checkRequest = self.client.get('/api/show_payment'
                                      , {'username': 'make_payment'}
                                      , format='json')
        returnData = json.loads(checkRequest.content.decode())
        self.assertEquals(len(returnData), 1)
        entry = returnData[0]
        self.assertEquals(entry['charity'], 'charilink@gmail.com')
        self.assertEquals(entry['currency'], 'USD')
        self.assertEquals(entry['amount'], 12)

        print("Make payment API passed.")
