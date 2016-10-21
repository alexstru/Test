from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class DatePickerWidgetTest(TestCase):
    """
    Check if DatePickerWidget is in the template
    """
    def test_birthday_widget(self):
        """ Check that template contains custom widget """
        self.admin = Client()
        self.admin.login(username='admin', password='admin')

        response = self.admin.get(reverse('hello:edit', kwargs={'pk': 1}))
        self.assertContains(response, '//code.jquery.com/ui/1.11.4/'
                                      'themes/smoothness/jquery-ui.css')
        self.assertContains(response, 'js/jquery-ui.min.js')
        self.assertContains(response, "$('#id_birthday').datepicker(")



