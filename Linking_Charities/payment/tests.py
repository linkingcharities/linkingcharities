from django.test import TestCase
from payment.models import *
from django.utils import timezone

# Create your tests here.

class PaymentTestCase(TestCase):

    def setUp(self):
        Payment.objects.create(username='ming'
                         , charity='charilink@gmail.com'
                         , currency='USD'
                         , amount='1'
                         , date=timezone.now())
        return

    def testGetPaymentAPIWithUser(self):
        
        response = self.client.get('/api/show_payment'
                                  , { 'username' : 'ming' }
                                  , format='json')

        print(response.content)
