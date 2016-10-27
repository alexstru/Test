
from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.hello.models import AboutMe, RequestContent,  ModelsChange
from apps.hello.utils import GetTestImage


class SignalsTest(TestCase):
    """
    Check signal processor for save log
    about creation/updating/deletion models objects
    """
    fixtures = ['test_data.json']

    def test_creation_log(self):
        """
        Check signal processor saves log
        about model object creation
        """
        ModelsChange.objects.all().delete()
        self.client.get(reverse('hello:home'))
        event = ModelsChange.objects.last()

        self.assertEqual(RequestContent.objects.all().count(), 11)
        self.assertEqual(ModelsChange.objects.all().count(), 1)
        self.assertEqual(event.action, 'CREATE')

    def test_updating_log(self):
        """
        Check signal processor saves log
        about model object updating
        """

        ModelsChange.objects.all().delete()
        profile = AboutMe.objects.first()
        profile.first_name = 'Leo'
        profile.email = 'leo.nardo@gmail.com'
        profile.photo = GetTestImage('test.png')
        profile.save()

        self.assertEqual(ModelsChange.objects.all().count(), 1)
        event = ModelsChange.objects.last()

        self.assertIn(profile._meta.object_name, event.model)
        self.assertEqual(event.action, 'UPDATE')

    def test_deletion_log(self):
        """
        Check signal processor saves log
        about model object deletion
        """
        ModelsChange.objects.all().delete()
        profile = AboutMe.objects.first()
        profile.delete()
        event = ModelsChange.objects.last()

        self.assertEqual(ModelsChange.objects.all().count(), 1)
        self.assertIn(profile._meta.object_name, event.model)
        self.assertEqual(event.action, 'DELETE')
