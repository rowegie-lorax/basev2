from django.test import TestCase
from user.models import User, Account, Branch, BranchSchedule

from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token

import json
import pprint
from datetime import datetime


class BranchScheduleTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        # a user must be logged-in
        self.client.post('/api/users/', {'email': 'valid@test.com',
                                         'phone_number': '9484749612',
                                         'password': 'secret',
                                         'user_type': 'A'})
        response = self.client.post(
            '/user_login/', {'username': 'valid@test.com', 'password': 'secret'})
        user = User.objects.get()
        user.is_active = True
        user.save()
        account = Account(name='Rowegie Lambojon', user=user)
        account.save()

        self.api_client = APIClient()
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get().key)
        self.api_client.login(email="valid@test.com", password='secret')

        self.now = datetime.now()

    def test_add_branch_schedule(self):
        response = self.api_client.post('/api/branch/', {"name": "branch 1",
                                                         "location": "somewhere"})

        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(response.status, 201)

        self.assertEqual(Branch.objects.count(), 1)
        self.assertEqual(Branch.objects.get(pk=id_created).name, "branch 1")
        self.assertEqual(Branch.objects.get(
            pk=id_created).branch_alias, "branch 1")

        response = self.api_client.post('/api/branch_schedule/', {
                                        "day": "tue", "date": "2017-07-11", "status": "OPEN", "start": "17:00:00", "end": "20:30:00", "branch": id_created})
        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(BranchSchedule.objects.count(), 1)
        self.assertEqual(BranchSchedule.objects.get(
            pk=id_created).status, "OPEN")

    def test_add_branch_schedule_with_duplicate_time(self):
        response = self.api_client.post('/api/branch/', {"name": "branch 1",
                                                         "location": "somewhere"})

        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(response.status, 201)

        self.assertEqual(Branch.objects.count(), 1)
        self.assertEqual(Branch.objects.get(pk=id_created).name, "branch 1")
        self.assertEqual(Branch.objects.get(
            pk=id_created).branch_alias, "branch 1")

        response = self.api_client.post('/api/branch_schedule/', {
                                        "day": "tue", "date": "2017-07-11", "status": "OPEN", "start": "17:00:00", "end": "20:30:00", "branch": id_created})
        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(BranchSchedule.objects.count(), 1)
        self.assertEqual(BranchSchedule.objects.get(
            pk=id_created).status, "OPEN")
        response = self.api_client.post('/api/branch_schedule/', {
                                        "day": "tue", "date": "2017-07-11", "status": "OPEN", "start": "17:00:00", "end": "20:30:00", "branch": id_created})
        pp = pprint.PrettyPrinter(indent=4)
        message = json.loads(response.content.decode('utf-8'))['message']
        success = json.loads(response.content.decode('utf-8'))['success']
        self.assertEqual(response.status, 400)
        self.assertEqual(BranchSchedule.objects.count(), 1)
        self.assertEqual(message, "Invalid Request")
        self.assertEqual(success, False)

    def test_update_branch_schedules(self):
        response = self.api_client.post('/api/branch/', {"name": "branch 1",
                                                         "location": "somewhere"})

        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(response.status, 201)

        self.assertEqual(Branch.objects.count(), 1)
        self.assertEqual(Branch.objects.get(pk=id_created).name, "branch 1")
        self.assertEqual(Branch.objects.get(
            pk=id_created).branch_alias, "branch 1")

        response = self.api_client.post('/api/branch_schedule/', {
                                        "day": "tue", "date": "2017-07-11", "status": "OPEN", "start": "17:00:00", "end": "20:30:00", "branch": id_created})
        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(BranchSchedule.objects.count(), 1)
        self.assertEqual(BranchSchedule.objects.get(
            pk=id_created).status, "OPEN")
        response = self.api_client.put('/api/branch_schedule/' + str(id_created) +'/', {
                                        "day": "2017-07-11", "status": "CLOSE", "start": "16:00:00", "end": "19:30:00", "branch": id_created})
        
        id_created = json.loads(response.content.decode('utf-8'))['id']
        self.assertEqual(response.status, 200)
        self.assertEqual(BranchSchedule.objects.count(), 1)
        self.assertEqual(BranchSchedule.objects.get(pk=id_created).status, "CLOSE")


    def test_delete_branch_schedules(self):
        pp = pprint.PrettyPrinter(indent=4)
        response = self.api_client.post('/api/branch/', {"name": "branch 1",
                                                         "location": "somewhere"})

        branch_id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(response.status, 201)

        self.assertEqual(Branch.objects.count(), 1)
        self.assertEqual(Branch.objects.get(pk=branch_id_created).name, "branch 1")
        self.assertEqual(Branch.objects.get(
            pk=branch_id_created).branch_alias, "branch 1")

        response = self.api_client.post('/api/branch_schedule/', {
                                        "day": "tue", "date": "2017-07-11", "status": "OPEN", "start": "17:00:00", "end": "20:30:00", "branch": branch_id_created})
        id_created = json.loads(response.content.decode('utf-8'))['data']['id']
        self.assertEqual(BranchSchedule.objects.count(), 1)
        self.assertEqual(BranchSchedule.objects.get(
            pk=id_created).status, "OPEN")
        response = self.api_client.delete('/api/branch_schedule/' + str(id_created) +'/', {"branch": branch_id_created})
        message = json.loads(response.content.decode('utf-8'))['message']
        self.assertEqual(response.status, 200)


    # def test_update_branch_with_duplicate_data(self):

    #     response = self.api_client.post('/api/branch/', {"name": "branch One",
    #                                                      "branch_alias": "branch One",
    #                                                      "location": "somewhere"})

    #     response = self.api_client.post('/api/branch/', {"name": "branch 1",
    #                                                      "branch_alias": "branch 1",
    #                                                      "location": "somewhere"})

    #     id_created = json.loads(response.content.decode('utf-8'))['data']['id']
    #     response = self.api_client.put('/api/branch/' + str(id_created) + '/', {"name": "branch One",
    #                                                                             "branch_alias": "branch One",
    #                                                                             "location": "anywhere",
    #                                                                             "phone": "+424242"})

    #     pp.pprint(json.loads(response.content.decode('utf-8')))
    #     message = json.loads(response.content.decode('utf-8'))['message']
    #     isUpdated = json.loads(response.content.decode('utf-8'))['success']

    #     self.assertEqual(response.status, 400)
    #     self.assertEqual(Branch.objects.count(), 2)
    #     self.assertEqual(
    #         message, "Branch name already exits. Please choose another name")
    #     self.assertEqual(isUpdated, False)

    # def test_retrieve_branch_specific_account(self):
    #     response = self.api_client.post('/api/branch/', {"name": "branch 1",
    #                                                      "branch_alias": "branch 1",
    #                                                      "location": "somewhere"})

    #     id_created = json.loads(response.content.decode('utf-8'))['data']['id']
    #     response = self.api_client.get('/api/branch/' + str(id_created) + '/')
    #     self.assertEqual(response.status, 200)
    #     retrieved = Branch.objects.get(pk=id_created)
    #     self.assertEqual(retrieved.name, "branch 1")
    #     self.assertEqual(retrieved.branch_alias, "branch 1")
    #     self.assertEqual(retrieved.location, "somewhere")

    # def test_delete_branch(self):
    #     response = self.api_client.post('/api/branch/', {"name": "branch 2",
    #                                                      "branch_alias": "branch 2",
    #                                                      "location": "somewhere"})
    #     self.assertEqual(Branch.objects.count(), 1)

    #     id_created = id_created = json.loads(
    #         response.content.decode('utf-8'))['data']['id']
    #     response = self.api_client.delete(
    #         '/api/branch/' + str(id_created) + '/', format='json')

    #     message = json.loads(response.content.decode('utf-8'))['message']
    #     isDeleted = json.loads(response.content.decode('utf-8'))['success']

    #     self.assertEqual(response.status, 200)
    #     self.assertEqual(Branch.objects.count(), 0)
    #     self.assertEqual(message, "Branch successfully deleted")
    #     self.assertEqual(isDeleted, True)
