from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    orig_link = models.URLField(
        null=False,
        help_text="Original link",
        verbose_name="orig_link"
    )
    domain_name = models.CharField(
        max_length=100,
        null=False,
        help_text="Domain name of original link",
        verbose_name="domain_name"
    )
    random_sequence = models.CharField(
        max_length=8,
        null=False,
        unique=True,
        help_text="Short link identifier",
        verbose_name="random_sequence"
    )
    link_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Link owner's id",
        verbose_name="link_owner"
    )
    creation_date = models.DateTimeField(
        default=datetime.utcnow,
        help_text="Short link creation time",
        verbose_name="creation_date"
    )
    life_time_end = models.DateTimeField(
        default=datetime.max,
        help_text="Time until which the link will be liquid",
        verbose_name="life_time_end"
    )
    link_tag = models.CharField(
        max_length=32,
        help_text="Link's tag",
        verbose_name="link_tag"
    )

    def __str__(self):
        return str(self.orig_link)

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"


class Transitions(models.Model):
    owner_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Owner of this link",
        verbose_name="owner_id"
    )
    link_id = models.ForeignKey(
        Link,
        on_delete=models.CASCADE,
        help_text="Identifier of link",
        verbose_name="link_id"
    )
    trans_time = models.DateTimeField(
        null=False,
        help_text="Transition time",
        verbose_name="trans_time"
    )

    def __str__(self):
        return str(self.owner_id)

    class Meta:
        verbose_name = "Transition"
        verbose_name_plural = "Transitions"
