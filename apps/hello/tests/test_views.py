from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from apps.hello.models import AboutMe, RequestContent, Thread
import json
from apps.hello.utils import GetTestImage, RemoveTestImages
from apps.hello.forms import ProfileUpdateForm

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

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_view_returns_200(self):
        " test view returns code 200 in response "
        response = self.client.get(reverse('hello:request'))
        self.assertEqual(response.status_code, 200)

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

        """ Check if there are empty ajax-data in the request.html """

        response = self.client.get(reverse('hello:request'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())

        self.assertEqual(data['dbcount'], 0)
        self.assertEqual(data['reqlogs'], [])

        """ Make 10 request and check ajax-data in the request.html """

        for i in range(10):
            self.client.get(reverse('hello:home'))

        request_path = RequestFactory().get('hello:home').build_absolute_uri()

        response = self.client.get(reverse('hello:request'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(response.content.decode())

        self.assertEqual(data['dbcount'], 10)
        self.assertTrue(data['reqlogs'][0]['path'] in request_path)
        self.assertContains(response, '"method": "GET"', 10, 200)


class ProfileEditViewTests(TestCase):
    """ profile editing view test case """

    def setUp(self):
        """ Set parametrs for ajax  """

        self.url = reverse('hello:edit', kwargs={'pk': 1})
        self.kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        self.fields_list = ('first_name', 'last_name', 'email',
                            'jabber', 'skype', 'photo', 'birthday')

    def test_form_in_edit_page(self):
        """ Test html on the edit profile page """

        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertIn('form', response.context)

        form = response.context['form']
        profile = AboutMe.objects.first()
        self.assertEqual(profile, form.instance)

    def test_image_resize(self):
        """
        Check that image is saved and resized to 200x200px
        """
        instance = AboutMe.objects.first()
        image = GetTestImage('test.png', 'PIL')

        # check that image is bigger than 200x200px
        self.assertGreater(image.height, 200)
        self.assertGreater(image.width, 200)

        form = ProfileUpdateForm(NORMAL,
                                 {'photo': GetTestImage('test.png')},
                                 instance=instance)

        self.assertTrue(form.is_valid())
        form.save()

        # check that image is resized to 200x200px
        profile = AboutMe.objects.first()
        image_resized = GetTestImage(profile.photo, 'PIL')
        self.assertLessEqual(image_resized.height, 200)
        self.assertLessEqual(image_resized.width, 200)

    def test_ajax_invalid_post(self):
        """ Test for ajax post with errors """

        data = dict.fromkeys(self.fields_list, '')

        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url, data, **self.kwargs)

        ERROR_MESSAGE = 'This field is required.'
        self.assertContains(response, ERROR_MESSAGE, 6, 400)

        profile = AboutMe.objects.first()

        for field in self.fields_list:
            self.assertNotEqual(profile.serializable_value(field),
                                data[field])

    def test_ajax_valid_post(self):
        """ Test for ajax valid post """

        data_list = ('Max',
                     'Johnson',
                     'max@gmail.com',
                     'max_jab',
                     'max_sk',
                     GetTestImage('test.png'),
                     '2016-01-01')

        data = dict(zip(self.fields_list, data_list))

        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url, data, **self.kwargs)

        self.assertEqual(response.status_code, 200)

        profile = AboutMe.objects.first()

        for field in self.fields_list[:-2]:
            self.assertEqual(profile.serializable_value(field),
                             data[field])


class TestChatView(TestCase):
    """ chat view test case """

    fixtures = ['test_data.json']

    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.url = reverse('hello:user_chat')

    def test_chat_is_returned(self):
        """ test view returns the correct template """

        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'dialogs.html')
        self.assertTrue('users' in self.response.context)

    def test_chat_with_non_existant_threads(self):
        """ test view when there are no threads """

        self.response = self.client.get(self.url)
        self.assertFalse('threads' in self.response.context)
        self.assertTrue('There are no dialogs yet'
                        in self.response.content)

    def test_chat_with_threads(self):
        """ test view when threads exists"""

        thread = Thread()
        thread.save()
        thread.participants.add(1, 2)
        self.assertEqual(Thread.objects.count(), 1)

        print(thread.participants.all())

        self.response = self.client.get(self.url)
        self.assertTrue('threads' in self.response.context)
        self.assertEqual(self.response.context['threads'][0].participants,
                         thread.participants)

    def test_ajax_post(self):
        """
        Test ajax post after sending new message
        """

        response = self.client.post(reverse('hello:user_chat'),
                                    data={'sender': 'Jaroslav',
                                          'receiver': 'Andrey',
                                          'date': 'Nov 26, 2016, 9:00:00 AM',
                                          'text': 'There is news', },
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.reason_phrase, 'OK')

        RemoveTestImages()
