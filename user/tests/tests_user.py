from django.test import TestCase
from user.models import User

from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token

import json
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)


class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        # a user must be logged-in
        self.client.post('/api/users/', {'email': 'valid@test.com',\
                                         'phone_number': '9484749612',\
                                         'password': 'secret',\
                                         'user_type': 'A'})
        response = self.client.post(
            '/user_login/', {'username': 'valid@test.com', 'password': 'secret'})
        user = User.objects.get()
        user.is_active = True
        user.save()
        self.api_client = APIClient()
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get().key)
        self.api_client.login(email="valid@test.com", password='secret')

        self.now = datetime.now()

    def test_register_fail_phone_number_exist(self):
        response = self.client.post('/api/users/', {'email': 'testing@gmail.com',
                                                    'phone_number': '9484749612',
                                                    'password': 'secret',
                                                    'user_type': 'A'})
        self.assertEqual(response.status,  400)

    def test_register_fail_email_exist(self):
        response = self.client.post('/api/users/', {'email': 'valid@test.com',
                                                    'phone_number': '9167991309',
                                                    'password': 'secret',
                                                    'user_type': 'A'})
        self.assertEqual(response.status,  400)

    def test_register_fail_email_phone_number_exist(self):
        response = self.client.post('/api/users/', {'email': 'valid@test.com',
                                                    'phone_number': '9484749612',
                                                    'password': 'secret',
                                                    'user_type': 'A'})
        self.assertEqual(response.status,  400)

    def test_register_success(self):
        response = self.client.post('/api/users/', {'email': 'success@success.com',
                                                    'phone_number': '9167991309',
                                                    'password': 'success',
                                                    'user_type': 'A'})
        pp.pprint(json.loads(response.content.decode('utf-8')))
        pp.pprint(response.status)
        self.assertEqual(response.status,  201)

    def test_update(self):
        self.client.post('/api/users/', {'email': 'update@test.com',
                                         'phone_number': '9747878525',
                                         'password': 'secret01',
                                         'user_type': 'A'})
        response = self.client.post('/user_login/', {'username': 'update@test.com',
                                                     'password': 'secret01',
                                                     'user_type': 'A'})
        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        response = self.api_client.put('/api/users/' + str(id_created) + '/', {'email': 'valid@update.com',
                                                                               'phone_number': '9167991309',
                                                                               'password': 'secret',
                                                                               'user_type': 'A'
                                                                               })
        self.assertEqual(response.status,  200)

    def test_delete(self):
        self.client.post('/api/users/', {'email': 'delete@test.com',
                                         'phone_number': '9747878525',
                                         'password': 'secret01',
                                         'user_type': 'A'})
        response = self.client.post('/user_login/', {'username': 'delete@test.com',
                                                     'password': 'secret01',
                                                     'user_type': 'A'})
        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        response = self.api_client.delete(
            '/api/users/' + str(id_created) + '/')
        self.assertEqual(response.status,  200)

    