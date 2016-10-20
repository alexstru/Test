from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from apps.hello.models import AboutMe, RequestContent
import json
from django.db.models import ImageField


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


class TestRequestsDataView(TestCase):
    """ hard_coded_requests view test case """

    def test_view_returns_200(self):
        " test view returns code 200 in response "
        response = self.client.get(reverse('hello:request'))
        self.assertEqual(response.status_code, 200)

    def test_requests_list_in_context(self):
        """ test view response context contains
        list of 10 request info objects """

        # fill template with 11 requests
        for i in range(11):
            response = self.client.get(reverse('hello:request'))

        # check for 10 objects in context
        self.assertTrue('object_list' in response.context)
        self.assertEqual(len(response.context['object_list']), 10)

    def test_no_entries_requestcontent_in_db(self):
        """ check correct reaction if there are
        no requestcontent entries in the db"""

        RequestContent.objects.all().delete()
        db = RequestContent.objects.all()
        self.assertEqual(len(db), 0)

        response = self.client.get(reverse('hello:request'))
        self.assertTrue('There is no entries in the db yet'
                        in response.content)

    def test_ajax(self):
        """Requests page updates asynchronously
            as new requests come in
        """
        RequestContent.objects.all().delete()
        response = self.client.get(reverse('hello:request'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())

        self.assertEqual(data['dbcount'], 0)
        self.assertEqual(data['reqlogs'], [])

        self.client.get(reverse('hello:home'))
        response = self.client.get(reverse('hello:request'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())

        self.assertEqual(data['dbcount'], 1)
        self.assertTrue('http://testserver/' in data['reqlogs'][0]['path'])
        self.assertContains(response, '"method": "GET"', 1, 200)


class ProfileEditViewTests(TestCase):
    """ profile editing view test case """

    def test_form_in_edit_page(self):
        """ Test html on the edit profile page """

        self.client = Client()
        response = self.client.get(reverse('hello:edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertIn('form', response.context)

        form = response.context['form']
        profile = AboutMe.objects.first()
        self.assertEqual(profile, form.instance)

    def test_image_field(self):
        """ Check that AboutMe instance have ImageField """

        photo = AboutMe._meta.get_field('photo')
        self.assertIsInstance(photo, ImageField)
