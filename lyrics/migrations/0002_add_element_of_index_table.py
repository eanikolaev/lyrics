# -*- coding: utf-8 -*-
__author__ = 'a.melnikov'

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IndexElement'
        db.create_table(u'lyrics_indexelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'lyrics', ['IndexElement'])

        # Adding M2M table for field song on 'IndexElement'
        m2m_table_name = db.shorten_name(u'lyrics_indexelement_song')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('indexelement', models.ForeignKey(orm[u'lyrics.indexelement'], null=False)),
            ('song', models.ForeignKey(orm[u'lyrics.song'], null=False))
        ))
        db.create_unique(m2m_table_name, ['indexelement_id', 'song_id'])


    def backwards(self, orm):
        # Deleting model 'IndexElement'
        db.delete_table(u'lyrics_indexelement')

        # Removing M2M table for field song on 'IndexElement'
        db.delete_table(db.shorten_name(u'lyrics_indexelement_song'))


    models = {
        u'lyrics.indexelement': {
            'Meta': {'object_name': 'IndexElement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'song': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lyrics.Song']", 'symmetrical': 'False'}),
            'term': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'lyrics.song': {
            'Meta': {'ordering': "['title']", 'object_name': 'Song'},
            'aid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['lyrics']