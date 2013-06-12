# coding=utf-8

import json

from django.test import TestCase

from parliamentarygroup import factories


class GroupResourceTest(TestCase):
    url = '/api/v1/group/'

    def setUp(self):
        self.group1 = factories.GroupFactory()
        self.group2 = factories.GroupFactory()

        self.party1 = factories.PartyFactory()
        self.party2 = factories.PartyFactory()
        self.party3 = factories.PartyFactory()

        self.groupmember1 = factories.GroupMemberFactory(
            group=self.group1, party=self.party1)
        self.groupmember2 = factories.GroupMemberFactory(
            group=self.group2, party=self.party2)
        self.groupmember3 = factories.GroupMemberFactory(
            group=self.group1, party=self.party3)
        self.groupmember4 = factories.GroupMemberFactory(
            group=self.group1, party=self.party3)

    def test_access(self):
        """
            Test all GET possibilities and filters
        """
        response = self.client.get(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 2)

        response = self.client.get(
            self.url + '%s/' % self.group1.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], self.group1.pk)
        self.assertIn('members', response_json)
        self.assertEqual(len(response_json['members']), 3)

        response = self.client.get(
            self.url + '%s/' % self.group2.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['members']), 1)

        response = self.client.get(
            self.url + '?id=%s' % self.group1.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 1)
        self.assertEqual(response_json['objects'][0]['id'], self.group1.pk)

        response = self.client.get(
            self.url + '?name=%s' % self.group1.name, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 1)
        self.assertEqual(response_json['objects'][0]['id'], self.group1.pk)

        response = self.client.get(
            self.url + '?name__startswith=%s' % self.group1.name.split('_')[0],
            {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 2)

        response = self.client.get(
            self.url + '?name=%s' % 'uglygroup', {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 0)

    def test_modification(self):
        """
            No modification is allowed
        """
        response = self.client.post(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.post(
            self.url + '%s/' % self.group1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(
            self.url + '%s/' % self.group1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
            self.url + '%s/' % self.group1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)


class PartyResourceTest(TestCase):
    url = '/api/v1/party/'

    def setUp(self):
        self.group1 = factories.GroupFactory()
        self.group2 = factories.GroupFactory()

        self.party1 = factories.PartyFactory()
        self.party2 = factories.PartyFactory()
        self.party3 = factories.PartyFactory()

        self.groupmember1 = factories.GroupMemberFactory(
            group=self.group1, party=self.party1)
        self.groupmember2 = factories.GroupMemberFactory(
            group=self.group2, party=self.party2)
        self.groupmember3 = factories.GroupMemberFactory(
            group=self.group1, party=self.party3)
        self.groupmember4 = factories.GroupMemberFactory(
            group=self.group1, party=self.party3)

    def test_access(self):
        """
            Test all GET possibilities and filters
        """
        response = self.client.get(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 3)

        response = self.client.get(
            self.url + '%s/' % self.party1.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], self.party1.pk)

        response = self.client.get(
            self.url + '%s/' % self.party2.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)

        response = self.client.get(
            self.url + '?id=%s' % self.party1.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 1)
        self.assertEqual(response_json['objects'][0]['id'], self.party1.pk)

        response = self.client.get(
            self.url + '?name=%s' % self.party1.name, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 1)
        self.assertEqual(response_json['objects'][0]['id'], self.party1.pk)

        response = self.client.get(
            self.url + '?name__startswith=%s' % self.party1.name.split('_')[0],
            {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 3)

        response = self.client.get(
            self.url + '?name=%s' % 'uglygroup', {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 0)

    def test_modification(self):
        """
            No modification is allowed
        """
        response = self.client.post(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.post(
            self.url + '%s/' % self.party1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(
            self.url + '%s/' % self.party1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
            self.url + '%s/' % self.party1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)


class GroupMemberResourceTest(TestCase):
    url = '/api/v1/groupmember/'

    def setUp(self):
        self.group1 = factories.GroupFactory()
        self.group2 = factories.GroupFactory()

        self.party1 = factories.PartyFactory()
        self.party2 = factories.PartyFactory()
        self.party3 = factories.PartyFactory()

        self.groupmember1 = factories.GroupMemberFactory(
            group=self.group1, party=self.party1)
        self.groupmember2 = factories.GroupMemberFactory(
            group=self.group2, party=self.party2)
        self.groupmember3 = factories.GroupMemberFactory(
            group=self.group1, party=self.party3)
        self.groupmember4 = factories.GroupMemberFactory(
            group=self.group1, party=self.party3)

    def test_access(self):
        """
            Test all GET possibilities and filters
        """
        response = self.client.get(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 4)

        response = self.client.get(
            self.url + '%s/' % self.party1.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], self.party1.pk)

        response = self.client.get(
            self.url + '%s/' % self.party2.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)

    def test_modification(self):
        """
            No modification is allowed
        """
        response = self.client.post(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
            self.url, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.post(
            self.url + '%s/' % self.party1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(
            self.url + '%s/' % self.party1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
            self.url + '%s/' % self.party1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)
