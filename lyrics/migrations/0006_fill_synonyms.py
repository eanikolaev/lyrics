# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import os
import re
from lyrics.models import Song, IndexElement

# -----------------------------------------------------------------------------pymorphy
from pymorphy.contrib import tokenizers
from pymorphy import get_morph                      # Морф анализатор https://pythonhosted.org/pymorphy/intro.html
morph = get_morph('/home/antre/pymorphy_dicts/')    # Директория со словарями для pymorphy

DIR_OF_COLLECT_DATA = os.path.dirname(os.path.abspath(__file__))[:-17] + "collect_data/"
FILE_WITH_SYNONYMS = DIR_OF_COLLECT_DATA + "synonims.txt"


class Migration(DataMigration):

    def forwards(self, orm):

        fi = open(FILE_WITH_SYNONYMS, "rb")
        for line in fi:
            try:
                term, synonyms = line.decode("cp1251")[:-2].upper().split('|', 2)
                print term
            except ValueError:
                continue
            synonyms = synonyms.split('.')[0]                   # Отсекаются всякие антонимы
            synonyms = re.sub('\([^)]*\)', '()', synonyms)      # Отсекаются всякие слова в скобках
            list_of_synonyms = synonyms.split(',')

            # Ищем слово в базе, чтобы начать прикручивать к нему синонимы
            try:
                w = IndexElement.objects.get(term=term)

                for s in list_of_synonyms:
                    try:
                        syn = IndexElement.objects.get(term=s)
                        w.synonyms.add(syn)
                    except IndexElement.DoesNotExist:
                        pass
            except IndexElement.DoesNotExist:
                pass
        fi.close()
        print "Synonyms added to database"

    def backwards(self, orm):
        "Write your backwards methods here."
        for w in IndexElement.objects.all():
            w.synonyms.clear()

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
    symmetrical = True
