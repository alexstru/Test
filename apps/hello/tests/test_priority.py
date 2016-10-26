
from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.hello.models import RequestContent
import json


class PriorityTest(TestCase):
    """
    Tests priority field in RequestContent model
    """

    def test_saving_priority(self):
        """
        Test for saving priority field in RequestContent model
        """

        request_info = RequestContent.objects.first()

        self.assertEqual(request_info.priority, 0)
        request_info.priority = 1
        request_info.save()

        request_info = RequestContent.objects.first()

        self.assertEqual(request_info.priority, 1)

    def test_ajax_post(self):
        """
        Test ajax when user click on priority-checkbox
        """

        self.client.login(username='admin', password='admin')

        ''' Check if priority = 0 in the request with id = 10 '''
        response = self.client.get(reverse('hello:request'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())

        self.assertEqual(data['reqlogs'][0]['id'], 10)
        self.assertEqual(data['reqlogs'][0]['priority'], 0)

        ''' Post priority = 1 for the request with pk = 10 '''
        response = self.client.post(reverse('hello:request'),
                                    data={"pk": "10", "priority": "1", },
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEquals(response.content,
                          '{"priority": "1", "link_id": "#priority_10"}')

        ''' Check if priority = 1 in the request with id = 10 '''
        response = self.client.get(reverse('hello:request'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())

        self.assertEqual(data['reqlogs'][0]['id'], 10)
        self.assertEqual(data['reqlogs'][0]['priority'], 1)

    def test_requests_sorting_by_priority(self):
        """
        Test for requests sorting by priority in the template
        """

        self.client.login(username='admin', password='admin')

        ''' Check if RequestContent has 10 requests with priority = 0 '''

        response = self.client.get(reverse('hello:request'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())
        self.assertEqual(data['dbcount'], 10)

        for i in range(10):
            self.assertEqual(data['reqlogs'][i]['priority'], 0)

        ''' Fill 5 requests in RequestContent with priority = 1 '''

        pk_first = RequestContent.objects.first().pk

        for i in range(pk_first, pk_first+5):
            webrequest = RequestContent.objects.get(pk=i)
            webrequest.priority = 1
            webrequest.save()

        ''' Make ajax sorting by high priority '''

        response = self.client.get(reverse('hello:request') + '?priority=1',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())
        webrequests = RequestContent.objects.all().order_by('-priority')

        for i in range(5):
            self.assertEqual(data['reqlogs'][i]['priority'],
                             webrequests[i].priority)
            self.assertEqual(webrequests[i].priority, 1)

        ''' Make ajax sorting by low priority '''

        response = self.client.get(reverse('hello:request') + '?priority=0',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())
        webrequests = RequestContent.objects.all().order_by('priority')

        for i in range(5):
            self.assertEqual(data['reqlogs'][i]['priority'],
                             webrequests[i].priority)
            self.assertEqual(webrequests[i].priority, 0)
