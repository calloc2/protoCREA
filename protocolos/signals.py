from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Protocolo
from .sitac_service import SITACService


@receiver(post_save, sender=Protocolo)
def submit_protocolo_to_sitac_on_create(sender, instance: Protocolo, created: bool, **kwargs):
    # Only submit on create and only for finalistic types
    if not created:
        return
    if instance.tipo not in ('finalistico_pf', 'finalistico_pj'):
        return

    sitac_service = SITACService()
    data = sitac_service.create_protocolo_data(instance)
    success, response = sitac_service.submit_protocolo(data)
    if success and response and 'protocolo' in response:
        # Save SITAC protocol number if returned
        Protocolo.objects.filter(pk=instance.pk).update(protocolo_sitac=response['protocolo'])


