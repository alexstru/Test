
from django.core.management.base import NoArgsCommand
from django.db.models import get_models


class Command(NoArgsCommand):
    """
    Command for print models and counting number of objects
    """
    help = 'Prints all project models and the count of objects in every model'

    def handle_noargs(self, **options):
        self.stdout.write('Model name: | Objects amount:')
        list_models = get_models(include_auto_created=True)

        for model in list_models:
            message = '{}: {}'.format(model._meta.object_name,
                                      model.objects.all().count())
            error_message = 'error: ' + message

            self.stdout.write(message)
            self.stderr.write(error_message)
