# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field synonyms on 'IndexElement'
        m2m_table_name = db.shorten_name(u'lyrics_indexelement_synonyms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_indexelement', models.ForeignKey(orm[u'lyrics.indexelement'], null=False)),
            ('to_indexelement', models.ForeignKey(orm[u'lyrics.indexelement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_indexelement_id', 'to_indexelement_id'])

        # Adding field 'Song.linked_movie'
        db.add_column(u'lyrics_song', 'linked_movie',
                      self.gf('django.db.models.fields.TextField')(default=None, max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Song.rude'
        db.add_column(u'lyrics_song', 'rude',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Removing M2M table for field synonyms on 'IndexElement'
        db.delete_table(db.shorten_name(u'lyrics_indexelement_synonyms'))

        # Deleting field 'Song.linked_movie'
        db.delete_column(u'lyrics_song', 'linked_movie')

        # Deleting field 'Song.rude'
        db.delete_column(u'lyrics_song', 'rude')


    models = {
        u'lyrics.indexelement': {
            'Meta': {'ordering': "['term']", 'object_name': 'IndexElement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'song': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lyrics.Song']", 'symmetrical': 'False'}),
            'synonyms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'im_syn_of'", 'symmetrical': 'False', 'to': u"orm['lyrics.IndexElement']"}),
            'term': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'lyrics.song': {
            'Meta': {'ordering': "['title']", 'object_name': 'Song'},
            'aid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_movie': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {}),
            'rude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['lyrics']