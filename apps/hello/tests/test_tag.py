
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import Context, Template, TemplateSyntaxError

from apps.hello.models import AboutMe
from apps.hello.templatetags.profile_admin_editing import edit_link


class TemplateTagTest(TestCase):
    """
    Test for template tag edit_link
    that renders the link to object's admin edit page
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.home_url = reverse('hello:home')
        self.profile = AboutMe.objects.first()
        self.anyobject = self.profile
        self.super_link = '{0}{1}/{2}/{3}/'.format(
            reverse('admin:index'),
            self.anyobject._meta.app_label,
            self.anyobject._meta.model_name,
            self.anyobject.pk)

    def test_tag_is_in_the_template(self):
        """
        The template contains custom tag
        """

        template = Template(
          '{% load profile_admin_editing %}{% edit_link profile %}')

        context = Context({'profile': self.profile})

        self.assertEqual(self.super_link, template.render(context))

    def test_rendered_link_is_in_the_template(self):
        """
        Find in the template rendered link to object's admin edit page
        """
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.home_url)
        tag_link = edit_link(self.profile)

        self.assertIn(self.super_link, response.content)
        self.assertEqual(tag_link, self.super_link)

    def test_tag_with_invalid_object(self):
        """
        If custom tag get invalid object
        than it must redirect to main page
        """
        with self.assertRaises(TemplateSyntaxError):
            edit_link('anyobject')
