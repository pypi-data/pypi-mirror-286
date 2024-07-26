from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions


class PrestationStep(Model):
    is_template = models.BooleanField(default=False)

    @property
    def name(self):
        if self.steps:
            names = [
                step.step.name
                for step in sorted(self.steps.all(), key=lambda step: step.order)
            ]
            return " > ".join(names)
        else:
            return self.urlid

    def __str__(self):
        try:
            if self.is_template:
                return "Template: {}".format(self.name)
            if self.prestation:
                return "{} ({})".format(self.prestation, self.urlid)
            return self.urlid
        except Exception:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("Prestation Related Step")
        verbose_name_plural = _("Prestation Related Steps")

        serializer_fields = ["@id", "is_template", "name", "steps"]
        nested_fields = ["steps"]
        rdf_type = "sib:PrestationTemplate"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["prestation"]
        depth = 2
