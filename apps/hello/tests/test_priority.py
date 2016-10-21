
from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.hello.models import RequestContent


class PriorityTest(TestCase):
    """
    Tests priority field in RequestContent model
    """

    def test_saving_priority(self):
        """
        Test for saving priority field in RequestContent model
        """
        self.client.get(reverse('hello:request'))
        request_info = RequestContent.objects.first()

        self.assertEqual(request_info.priority, 0)
        request_info.priority = 1
        request_info.save()

        request_info = RequestContent.objects.first()

        self.assertEqual(request_info.priority, 1)
