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

    photo = models.ImageField(
        upload_to='photo',
        null=False,
        blank=True,
        verbose_name=u"Фото",
        default='static/img/user_default.png')

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class RequestContent(models.Model):
    ''' RequestContent Model	'''

    method = models.CharField(max_length=7)
    path = models.TextField('Path', max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField('Status code', max_length=3)

    def __unicode__(self):
        return u"%s %s" % (self.path, self.date)
