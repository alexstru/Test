# -*- coding: utf-8 -*-

from django.db import models
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor
from south.modelsinspector import add_introspection_rules


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

    photo = fields.ImageField(
        upload_to='photo',
        null=False,
        blank=True,
        verbose_name=u"Photo",
        dependencies=[
            FileDependency(processor=ImageProcessor(
            scale={'max_width': 200, 'max_height': 200}))
        ])

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class RequestContent(models.Model):
    ''' RequestContent Model	'''

    method = models.CharField(max_length=7)
    path = models.TextField('Path', max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField('Status code', max_length=3)
    priority = models.IntegerField(max_length=1, default=0)

    def __unicode__(self):
        return u"%s %s" % (self.path, self.date)


class ModelsChange(models.Model):
    ''' Model with entries about creation/updating/deletion
    in AboutMe/RequestContent Models '''

    model = models.CharField(max_length=10)
    datetime = models.DateTimeField(auto_now=True, auto_now_add=True)
    action = models.CharField(max_length=10)


add_introspection_rules([], ["^smartfields\.fields\.ImageField"])
