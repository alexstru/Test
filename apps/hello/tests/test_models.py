# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.hello.models import AboutMe
from django.utils.encoding import smart_unicode


class AboutMeModelTest(TestCase):
    """Test AboutMe model"""

    def test_unicode(self):
        """ test that __unicode__ returns
        <first_name last_name> """

        bio = AboutMe(first_name=u'Розробник', last_name=u'Джанго')
        self.assertEqual(smart_unicode(bio), u'Розробник Джанго')
