
from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from django.db.models import get_models


class CouuntObjectsTest(TestCase):
    """ Check print_objects_count command to print models
        and calculate objects amount
    """

    def test_print_objects_count_command(self):
        """ Check the command to print models and
            calculate objects amount
        """
        STDOUT = StringIO()
        STDERR = StringIO()

        call_command('print_objects_count', stdout=STDOUT)
        call_command('print_objects_count', stderr=STDERR)
        result_out = STDOUT.getvalue()
        result_err = STDERR.getvalue()
        list_models = get_models(include_auto_created=True)

        for model in list_models:
            self.assertIn(model._meta.object_name, result_out)
            self.assertIn('error: ' + model._meta.object_name, result_err)

        self.assertIn('AboutMe: 1', result_out)
        self.assertIn('RequestContent: 10', result_out)
        self.assertIn('User: 1', result_out)
        self.assertIn('error: AboutMe: 1', result_err)
        self.assertIn('error: RequestContent: 10', result_err)
        self.assertIn('error: User: 1', result_err)
