# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RoomsModel.spots'
        db.alter_column(u'smyt_roomsmodel', 'spots', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'LanguagesModel.spots'
        db.alter_column(u'smyt_languagesmodel', 'spots', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UsersModel.paycheck'
        db.alter_column(u'smyt_usersmodel', 'paycheck', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UsersModel.date_joined'
        db.alter_column(u'smyt_usersmodel', 'date_joined', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'RoomsModel.spots'
        db.alter_column(u'smyt_roomsmodel', 'spots', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'LanguagesModel.spots'
        db.alter_column(u'smyt_languagesmodel', 'spots', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'UsersModel.paycheck'
        db.alter_column(u'smyt_usersmodel', 'paycheck', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'UsersModel.date_joined'
        db.alter_column(u'smyt_usersmodel', 'date_joined', self.gf('django.db.models.fields.CharField')(max_length=20))

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