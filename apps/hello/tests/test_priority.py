
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
