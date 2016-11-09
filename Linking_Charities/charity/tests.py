from django.test import TestCase
from rest_framework.test import APIRequestFactory
from charity.models import *

class  CharityTestCase(TestCase):
  
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
        print "Get all Charity test passed."
