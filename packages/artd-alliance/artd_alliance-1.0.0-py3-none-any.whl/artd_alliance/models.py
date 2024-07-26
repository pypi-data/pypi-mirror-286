import datetime
import os
import random
import string
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_partner.models import Partner
from artd_location.models import City
from django.db.models.signals import pre_save
from django.dispatch import receiver
from artd_alliance.context_processors import get_current_user

BENEFIT_TYPE = (
    ("discount", _("Discount")),
    ("fixed", _("Fixed")),
)

BENEFIT_STATUS_CHOICES = (
    ('active', _('Active')),
    ('requested', _('Requested')),
    ('under_review', _('Under review')),
    ('denied', _('Denied')),
    ('inactive', _('Inactive')),
    ('created', _('Created')),
)
def ally_image_path(instance, filename, *args, **kwargs):
    now = datetime.datetime.now()
    current_timestamp = str(round(int(datetime.datetime.timestamp(now))))
    pool = string.ascii_letters
    hash_identifier = "".join(random.choice(pool) for i in range(4))
    return os.path.join("images", "allies", current_timestamp + "" + hash_identifier + "" + filename)

class AllianceBaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        help_text=_("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        help_text=_("Updated at"),
        auto_now=True,
    )
    status = models.BooleanField(
        _("Status"),
        help_text=_("Status"),
        default=True,
    )

    class Meta:
        abstract = True


class Ally(AllianceBaseModel):
    name = models.CharField(
        _("Name"),
        help_text=_("Name of partner"),
        max_length=150,
    )
    dni = models.CharField(
        _("Dni"),
        help_text=_("DNI of partner"),
        max_length=20,
    )
    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        _("Email"),
        help_text=_("Email of partner"),
        max_length=254,
    )
    city_new = models.ForeignKey(
        City,
        on_delete=models.DO_NOTHING,
        related_name="+",
        null=True,
        blank=True,
    )
    address = models.CharField(
        _("Address"),
        help_text=_("Address of partner"),
        max_length=250,
    )
    logo = models.ImageField(
        _("Logo"),
        help_text=_("Logo ally"),
        upload_to=ally_image_path,

    )

    class Meta:
        verbose_name = _("Ally")
        verbose_name_plural = _("Allies")

    def __str__(self):
        return self.name


class Alliance(AllianceBaseModel):
    ally = models.ForeignKey(
        Ally,
        verbose_name=_("Ally"),
        help_text=_("Ally"),
        on_delete=models.CASCADE,
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Partner of headquarter"),
        on_delete=models.CASCADE,
    )
    service = models.CharField(
        _("Service"),
        help_text=_("Service"),
        max_length=150,
    )
    benefit = models.CharField(
        _("Benefit"),
        help_text=_("Benefit"),
        max_length=150,
    )
    benefit_type = models.CharField(
        _("Benefit Type"),
        help_text=_("Benefit Type"),
        max_length=255,
        choices=BENEFIT_TYPE,
        default="fixed",
    )
    alliance_status = models.CharField(
        _("Benefit Status"),
        help_text=_("Benefit Status"),
        max_length=255,
        choices=BENEFIT_STATUS_CHOICES,
        default='inactive'
    )
    code_alliance = models.SlugField(
        _("Code"),
        help_text=_("Code Alliance"),
        max_length=150,
    )

    class Meta:
        verbose_name = _("Alliance")
        verbose_name_plural = _("Alliances")

    def __str__(self):
        return f"{self.ally}"


class AllianceStatusChange(AllianceBaseModel):
    alliance = models.ForeignKey(
        Alliance,
        verbose_name=_("Alliance"),
        help_text=_("The alliance whose status has changed"),
        on_delete=models.CASCADE,
    )
    new_status = models.CharField(
        _("Status"),
        help_text=_("Status"),
        max_length=255,
        choices=BENEFIT_STATUS_CHOICES,
        default='inactive'
    )
    old_status = models.CharField(
        _("Old Status"),
        help_text=_("Old Status"),
        max_length=255,
        choices=BENEFIT_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    change_date = models.DateTimeField(
        _("Change Date"), 
        auto_now_add=True
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
    )

    class Meta:
        verbose_name = _("Alliance Status Change")
        verbose_name_plural = _("Alliance Status Changes")

    def __str__(self):
        return f"{self.alliance} - {self.new_status}"

            

@receiver(pre_save, sender=Alliance)
def create_alliance_status_change(sender, instance, **kwargs):
    user = get_current_user()
    print(user)
    if not instance.pk:
        print("Va a ser creado")
        return
    else:
        print("va a ser actualizado")
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        if old_instance.alliance_status != instance.alliance_status:
            AllianceStatusChange.objects.create(
                alliance = instance,
                old_status = old_instance.alliance_status,
                new_status = instance.alliance_status,
                changed_by = user
            )
            print(old_instance.alliance_status,instance.alliance_status)
        else:
            print(old_instance.alliance_status,instance.alliance_status)