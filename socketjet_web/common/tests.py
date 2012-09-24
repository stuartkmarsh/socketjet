"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from common.models import *

class ApiTest(TestCase):
    def SetUp(self):
        print 'setup'
        
    def test_api_creation(self):
        api_key = ApiAccount.create_api_key()
        self.assertEqual(len(api_key), 32)
        
         
