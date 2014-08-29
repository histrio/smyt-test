# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UsersModel'
        db.create_table(u'smyt_usersmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'smyt', ['UsersModel'])

        # Adding model 'RoomsModel'
        db.create_table(u'smyt_roomsmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'smyt', ['RoomsModel'])


    def backwards(self, orm):
        # Deleting model 'UsersModel'
        db.delete_table(u'smyt_usersmodel')

        # Deleting model 'RoomsModel'
        db.delete_table(u'smyt_roomsmodel')


    models = {
        u'smyt.roomsmodel': {
            'Meta': {'object_name': 'RoomsModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'smyt.usersmodel': {
            'Meta': {'object_name': 'UsersModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['smyt']