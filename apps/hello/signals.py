from apps.hello.models import ModelsChange
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


IGNORE_MODELS = [ContentType, ModelsChange]


@receiver(post_save)
def model_save_handler(sender, created, **kwargs):

    if sender in IGNORE_MODELS:
        return

    action = "CREATE" if created else "UPDATE"
    log = kwargs['instance']
    info = ""

    if sender.__name__ == "AboutMe":
        info = ": " + log.first_name + " " + log.last_name

    if sender.__name__ == "RequestContent":
        info = ": " + log.path

    if sender.__name__ == "Session":
        info = ": " + log.session_key

    if sender.__name__ == "LogEntry":
        log = kwargs['instance']
        info = ": in  " + log.content_type.__str__() +\
               " " + log.change_message

    models_changes = ModelsChange.objects.create(
        model=sender.__name__ + info,
        action=action
    )
    models_changes.save()


@receiver(post_delete)
def model_delete_handler(sender, **kwargs):

    if sender in IGNORE_MODELS:
        return

    models_changes = ModelsChange.objects.create(
        model=sender.__name__,
        action="DELETE"
    )
    models_changes.save()
