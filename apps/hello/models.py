# -*- coding: utf-8 -*-

from django.db import models


class AboutMe(models.Model):
    """ Profile Model """

    class Meta(object):
        verbose_name = u"Bio"
        verbose_name_plural = u"Biography"

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"First name")

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Last name")

    birthday = models.DateField(
        blank=False,
        verbose_name=u"Birthday",
        null=True)

    email = models.EmailField()

    jabber = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Jabber")

    skype = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Skype")

    bio = models.TextField(
        blank=True,
        verbose_name=u"About me")

    contacts = models.TextField(
        blank=True,
        verbose_name=u"Additional contacts")

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)
