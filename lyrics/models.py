from django.db import models
from django.utils.translation import ugettext_lazy as _


class Song(models.Model):
    aid      = models.IntegerField(_('aid'), unique=True)
    artist   = models.CharField(_('artist'), max_length=128)
    title    = models.CharField(_('title'), max_length=128)
    duration = models.IntegerField(_('duration'))
    url      = models.URLField(_('url'), max_length=100)
    lyrics   = models.TextField(_('lyrics'))

    def __unicode__(self):
        return self.artist + ' - ' + "'" + self.title + "'"

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')
        ordering = ['title',]


class IndexElement(models.Model):
    term = models.CharField(_('term'), unique=True, max_length=100)
    song = models.ManyToManyField(Song)
