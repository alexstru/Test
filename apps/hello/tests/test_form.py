from django.test import TestCase
from apps.hello.forms import ProfileUpdateForm
from apps.hello.models import AboutMe
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
from datetime import date


class ProfileUpdateFormTests(TestCase):

    def test_form_and_db_data_equal(self):
        """
        Check that form saves correct data
        """
        instance = AboutMe.objects.first()
        IMG_ROOT = os.path.join(settings.BASE_DIR, 'apps/hello/static/img/')
        photo = open(IMG_ROOT + 'test.png', 'rb')

        form = ProfileUpdateForm({"id": 1,
                                  "first_name": "Alex",
                                  "last_name": "Testenko",
                                  "birthday": date(1999, 9, 19),
                                  "email": "mail@alex.com",
                                  "jabber": "j",
                                  "skype": "s",
                                  "bio": "some text",
                                  "contacts": "Allo ullu olla"},
                                 {'photo': SimpleUploadedFile(photo.name,
                                                              photo.read())},
                                 instance=instance)

        self.assertTrue(form.is_valid())
        form.save()

        # check database and form data equals
        profile = AboutMe.objects.first()

        for field in profile._meta.get_all_field_names():
            value = getattr(profile, field)
            if field != "photo":
                self.assertEqual(value, form.data[field])

    def test_blank_and_invalid_data(self):
        """
        Send empty data and invalid date and check form
        for required fields and valid date
        """
        form = ProfileUpdateForm({'birthday': '1999-0919'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
                         {'first_name': [u'This field is required.'],
                          'last_name': [u'This field is required.'],
                          'birthday': [u'Enter a valid date.'],
                          'skype': [u'This field is required.'],
                          'jabber': [u'This field is required.'],
                          'email': [u'This field is required.']
                          })
