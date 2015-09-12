import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytweets.settings")
from django.test import TestCase
from django.test.client import Client


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page(self):
        data ={
            'username': 'for_testing',
            'email': '111f@abc.com',
            'password': '1234',
            'confirm_password': '1234'
        }
        response = self.client.post('/register', data)
        self.assertEqual(response.status_code, 301)
