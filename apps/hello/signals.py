from apps.hello.models import ModelsChange, AboutMe, RequestContent
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


MODELS = [AboutMe, RequestContent, Session, LogEntry]


@receiver(post_save)
def model_save_handler(sender, created, **kwargs):

    if sender not in MODELS:
        return

    action = "CREATE" if created else "UPDATE"
    info = ""

    if sender.__name__ == "AboutMe":
        profile = kwargs['instance']
        info = ": " + profile.first_name + " " + profile.last_name

    if sender.__name__ == "RequestContent":
        reqlog = kwargs['instance']
        info = ": " + reqlog.path

    if sender.__name__ == "Session":
        seslog = kwargs['instance']
        info = ": " + seslog.session_key

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

    if sender not in MODELS:
        return

    models_changes = ModelsChange.objects.create(
        model=sender.__name__,
        action="DELETE"
    )
    models_changes.save()
