from apps.hello.models import ModelsChange, AboutMe, RequestContent
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=AboutMe)
@receiver(post_save, sender=RequestContent)
def model_save_handler(sender, created, **kwargs):

    person = ""

    if sender.__name__ == "AboutMe":
        profile = kwargs['instance']
        person = ": " + profile.first_name + " " + profile.last_name

    action = "CREATE" if created else "UPDATE"
    info = sender.__name__ + person

    models_changes = ModelsChange.objects.create(
        model=info,
        action=action
    )
    models_changes.save()


@receiver(post_delete, sender=AboutMe)
@receiver(post_delete, sender=RequestContent)
def model_delete_handler(sender, **kwargs):
    models_changes = ModelsChange.objects.create(
        model=sender.__name__,
        action="DELETE"
    )
    models_changes.save()
