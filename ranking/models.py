# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Ranks(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    ranking_creation_date = models.DateTimeField('date created')
    rank = models.IntegerField(default=0)

    def __str__(self):
        return "{0} by {1} with rank: {2}".format(self.title,
                                                  self.artist,
                                                  self.rank)

    class Meta:
        verbose_name = "Rank"
        verbose_name_plural = "Ranks"
        ordering = ['-rank']
        unique_together = ("title", "artist")
