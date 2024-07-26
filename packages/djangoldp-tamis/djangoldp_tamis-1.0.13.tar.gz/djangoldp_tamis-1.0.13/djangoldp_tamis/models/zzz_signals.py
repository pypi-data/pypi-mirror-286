from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from djangoldp_tamis.models.prestation import Prestation
from djangoldp_tamis.models.prestation_step import PrestationStep
from djangoldp_tamis.models.step_to_template import StepToTemplate


@receiver(pre_save, sender=Prestation)
def reject_prestation_without_editorial_work(instance, **kwargs):
    if not instance.editorial_work:
        raise ValidationError({"editorial_work": "Veuillez spécifier une version"})


@receiver(post_save, sender=Prestation)
def apply_or_create_template_steps(instance, **kwargs):
    if instance.template_steps:
        if instance.template_steps.is_template:
            prestationsteps, created = PrestationStep.objects.get_or_create(
                prestation=instance
            )
            for step in prestationsteps.steps.all():
                step.delete()
            for step in instance.template_steps.steps.all():
                StepToTemplate.objects.create(
                    template=prestationsteps,
                    step=step.step,
                    order=step.order,
                    validated=step.validated,
                    validation_date=step.validation_date,
                )
        instance.template_steps = None
        instance.save()
    else:
        PrestationStep.objects.get_or_create(prestation=instance)


@receiver(post_delete, sender=Prestation)
def clear_unused_prestation_steps(**kwargs):
    PrestationStep.objects.filter(prestation=None, is_template=False).delete()
