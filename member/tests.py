# coding=utf-8

import json

from django.test import TestCase

from member import factories


class MemberResourceTest(TestCase):
    url = '/api/v1/member/'

    def setUp(self):
        self.member1 = factories.MemberFactory()
        self.member2 = factories.MemberFactory(
            name='MemberTest2', second_name='Test Name')

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
            self.url + '%s/' % self.member1.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], self.member1.pk)

        response = self.client.get(
            self.url + '?id=%s' % self.member1.id, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 1)
        self.assertEqual(response_json['objects'][0]['id'], self.member1.pk)

        response = self.client.get(
            self.url + '?name=%s' % self.member1.name, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 1)
        self.assertEqual(response_json['objects'][0]['id'], self.member1.pk)


        response = self.client.get(
            self.url + '?name__startswith=%s' % self.member1.name, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json['objects']), 1)

        response = self.client.get(
            self.url + '?name=%s' % 'uglyface', {},
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
            self.url + '%s/' % self.member1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(
            self.url + '%s/' % self.member1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
            self.url + '%s/' % self.member1.pk, {},
            content_type='application/json')
        self.assertEqual(response.status_code, 405)
