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
        self.user = User.objects.create(username='ming', password="ming")
        DonorAccount.objects.create(account=self.user)
        self.charity = Charity.objects.create(name = 'foo', register_id = 1,
                   type = 'E',
                   description = 'Some info', target = 'C',
                   paypal = 'foo@bar.com')
        Payment.objects.create(account_id = self.user.id
                         , paypal='charilink@gmail.com'
                         , charity_id = self.charity.id
                         , currency='USD'
                         , amount='1'
                         , date=self.time)
        return

    def testGetPaymentAPIWithUser(self):
        
        response = self.client.get('/api/show_payment'
                                  , { 'username' : 'ming', 'payment': '1' }
                                  , format='json')
        
        returnData = json.loads(response.content.decode())
        self.assertEquals(len(returnData),1)
        entry = returnData[0]
        self.assertEquals(entry['account_id'], self.user.id)
        self.assertEquals(entry['charity_id'], self.charity.id)
        self.assertEquals(entry['paypal'], 'charilink@gmail.com')
        self.assertEquals(entry['currency'], 'USD')
        self.assertEquals(entry['amount'], 1)
        self.assertEquals(dateparse.parse_datetime(entry['date']), self.time)
        
        print("Get payment API passed.")

    def testGetPaymentAPICanGetMultiplePayments(self):
        
        otherCharity = Charity.objects.create(name = 'someothercharity@gmail.com', register_id = 12345,
                   type = 'E',
                   description = 'testing get multiple payments', target = 'C',
                   paypal = 'someotherpaypal@gmail.com')

        Payment.objects.create(account_id=self.user.id
                         , paypal = otherCharity.paypal
                         , charity_id=otherCharity.id
                         , currency='USD'
                         , amount='23'
                         , date=timezone.now())

        Payment.objects.create(account_id=self.user.id
                         , paypal = otherCharity.paypal
                         , charity_id=otherCharity.id
                         , currency='USD'
                         , date=timezone.now())
        
        response = self.client.get('/api/show_payment/?username=ming'
                                   , {}
                                   , format='json')
        returnData = json.loads(response.content.decode())
        self.assertEquals(len(returnData), 3)

        print("Get payment API multiple payments passed.")

    def testMakePaymentAPICanProduceRecord(self):
        user = User.objects.create(username="make_payment", password = "ming")
        data = { 'item_name' : user.id
               , 'business': self.charity.paypal
               , 'charity_id': self.charity.id
               , 'mc_currency': 'USD'
               , 'payment_gross': '12' }
        
        request = self.client.post('/api/make_payment', data, format='json')
        
        checkRequest = self.client.get('/api/show_payment/?username=make_payment'
                                      , {}
                                      , format='json')
        returnData = json.loads(checkRequest.content.decode())
        self.assertEquals(len(returnData), 1)
        entry = returnData[0]
        self.assertEquals(entry['charity_id'], self.charity.id)
        self.assertEquals(entry['currency'], 'USD')
        self.assertEquals(entry['amount'], 12)
        self.assertEquals(entry['account_id'], user.id)
        self.assertEquals(Charity.objects.get(pk=self.charity.id).donations, 12)

        print("Make payment API passed.")
