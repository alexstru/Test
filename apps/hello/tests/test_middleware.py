from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.hello.models import RequestContent


class RequestContentMiddlewareTests(TestCase):

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_template(self):
        """ Check correct template """
        response = self.client.get(reverse('hello:request'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request.html')

    def test_request_data_collecting(self):
        '''
        Test if middleware fill database with request
        '''
        RequestContent.objects.all().delete()
        db = RequestContent.objects.all()
        self.assertEqual(len(db), 0)
        self.client.get('/')
        db = RequestContent.objects.all()
        self.assertTrue(db.count(), 1)
        self.assertEqual('GET', db[0].method)
        self.assertEqual(200, db[0].status_code)
