from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from apps.hello.models import AboutMe

NORMAL = {
    'first_name': 'Alex',
    'last_name': 'Strong',
    'birthday': '1979-09-09',
    'email': 'k6_alexstr@ukr.net',
    'jabber': 'jabber',
    'skype': 'skype',
    'bio': 'bio',
    'contacts': 'contacts'
}


class TestHomeView(TestCase):

    def setUp(self):
        # remember test browser
        self.client = Client()

        # remember url to homepage
        self.url = reverse('hello:home')

        self.sample = NORMAL
        AboutMe.objects.all().delete()
        self.first_profile = AboutMe.objects.create(**self.sample)

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
        self.assertEqual(hello.email, 'k6_alexstr@ukr.net')

    def test_first_entry_selection(self):
        """ check first entry selection
        when db have many entries"""

        # create second AboutMe entry in the db
        AboutMe.objects.create(**self.sample)

        self.assertEqual(len(AboutMe.objects.all()), 2)

        self.first_profile.first_name = 'Alex First'
        self.first_profile.save()

        self.response = self.client.get(self.url)

        hello = self.response.context['bio']
        self.assertEqual(hello.first_name, 'Alex First')

    def test_no_entries_aboutme_in_db(self):
        """ check correct reaction if there are
        no aboutme entries in the db"""

        AboutMe.objects.all().delete()
        db = AboutMe.objects.all()
        self.assertEqual(len(db), 0)

        self.response = self.client.get(self.url)
        self.assertTrue('There is no profile in the db'
                        in self.response.content)
