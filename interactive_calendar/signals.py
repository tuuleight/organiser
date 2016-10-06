from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Event


@receiver(post_save, sender=Event)
def my_callback(sender, instance, **kwargs):
    if kwargs['update_fields '] == 'invited':
        s = ('Hi %r! User %r invited you to join his event %r, taking place '
             'in %r') % (instance.invited[-1], instance.author,
                         instance.name, instance.place)
        return s
