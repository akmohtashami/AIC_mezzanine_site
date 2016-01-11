# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Competition(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    title = models.CharField(verbose_name=_('title'), max_length=200)
    site = models.OneToOneField(Site, verbose_name=_('site'), null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('competition')
        verbose_name_plural = _('competitions')


class Game(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    competition = models.ForeignKey('game.Competition', verbose_name=_('competition'))
    title = models.CharField(verbose_name=_('title'), max_length=200)
    players = models.ManyToManyField('base.Team', verbose_name=_('players'), through='game.GameTeam')
    config = models.FileField(verbose_name=_('config'))

    pre_games = models.ManyToManyField('game.Game', verbose_name=_('pre games'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')


class GameTeam(models.Model):
    team = models.ForeignKey('base.Team', verbose_name=_('team'))
    game = models.ForeignKey('game.Game', verbose_name=_('game'))

    score = models.IntegerField(verbose_name=_('score'))

    class Meta:
        ordering = ('score',)
