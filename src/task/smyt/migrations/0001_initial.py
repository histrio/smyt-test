# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LanguagesModel'
        db.create_table(u'smyt_languagesmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'smyt', ['LanguagesModel'])

        # Adding model 'UsersModel'
        db.create_table(u'smyt_usersmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('paycheck', self.gf('django.db.models.fields.IntegerField')()),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'smyt', ['UsersModel'])

        # Adding model 'RoomsModel'
        db.create_table(u'smyt_roomsmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'smyt', ['RoomsModel'])


    def backwards(self, orm):
        # Deleting model 'LanguagesModel'
        db.delete_table(u'smyt_languagesmodel')

        # Deleting model 'UsersModel'
        db.delete_table(u'smyt_usersmodel')

        # Deleting model 'RoomsModel'
        db.delete_table(u'smyt_roomsmodel')


    models = {
        u'smyt.languagesmodel': {
            'Meta': {'object_name': 'LanguagesModel'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        u'smyt.roomsmodel': {
            'Meta': {'object_name': 'RoomsModel'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        u'smyt.usersmodel': {
            'Meta': {'object_name': 'UsersModel'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['smyt']