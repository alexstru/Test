# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.hello.models import AboutMe, RequestContent
from django.utils.encoding import smart_unicode

NORMAL = {
    "method": "GET",
    "path": "/request/",
    "status_code": "200",
    "date": "October 18, 2016, 13:23"
}


class AboutMeModelTest(TestCase):
    """Test AboutMe model"""

    def test_unicode(self):
        """ test that __unicode__ returns
        <first_name last_name> """

        bio = AboutMe(first_name=u'Розробник', last_name=u'Джанго')
        self.assertEqual(smart_unicode(bio), u'Розробник Джанго')


class RequestContentModelTest(TestCase):
    """Test RequestContent model"""

    def setUp(self):
        self.normal_info = NORMAL
        self.new_info = RequestContent.objects.create(**self.normal_info)

    def test_fields(self):
        """ check model fields """
        for key in self.normal_info.keys():
            if key != 'date':
                self.assertEquals(unicode(self.normal_info[key]),
                                  getattr(self.new_info, key))

    def test_unicode_label(self):
        """ test __unicode__ """

        info = RequestContent(path=u'шлях_запиту',
                              date='July 18, 2016, 09:30 a.m.')
        self.assertEqual(smart_unicode(info),
                         u'шлях_запиту July 18, 2016, 09:30 a.m.')
