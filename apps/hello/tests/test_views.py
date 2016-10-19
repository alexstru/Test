from django.test import TestCase, Client
from django.core.urlresolvers import reverse

# Create your tests here.


class TestHomeView(TestCase):

    def setUp(self):
        # remember test browser
        self.client = Client()

        # remember url to homepage
        self.url = reverse('hello:home')

        # make request to the server to get homepage page
        self.response = self.client.get(self.url)

    def test_profile_is_returned(self):
        """ find bio in context """

        # have we received OK status from the server?
        self.assertEqual(self.response.status_code, 200)

        # check that view returned the bio (profile) in the context
        self.assertTrue('bio' in self.response.context)

    def test_email_in_context(self):
        """ check that email = k6_alexstr@ukr.net """

        # now check if we got proper email
        hello = self.response.context['bio']
        self.assertEqual(hello['email'], 'k6_alexstr@ukr.net')
