# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RoomsModel.name'
        db.delete_column(u'smyt_roomsmodel', 'name')

        # Adding field 'RoomsModel.department'
        db.add_column(u'smyt_roomsmodel', 'department',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)

        # Adding field 'RoomsModel.spots'
        db.add_column(u'smyt_roomsmodel', 'spots',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)

        # Deleting field 'LanguagesModel.name'
        db.delete_column(u'smyt_languagesmodel', 'name')

        # Adding field 'LanguagesModel.department'
        db.add_column(u'smyt_languagesmodel', 'department',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)

        # Adding field 'LanguagesModel.spots'
        db.add_column(u'smyt_languagesmodel', 'spots',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=20),
                      keep_default=False)

        # Adding field 'UsersModel.paycheck'
        db.add_column(u'smyt_usersmodel', 'paycheck',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=20),
                      keep_default=False)

        # Adding field 'UsersModel.date_joined'
        db.add_column(u'smyt_usersmodel', 'date_joined',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'RoomsModel.name'
        raise RuntimeError("Cannot reverse this migration. 'RoomsModel.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'RoomsModel.name'
        db.add_column(u'smyt_roomsmodel', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=20),
                      keep_default=False)

        # Deleting field 'RoomsModel.department'
        db.delete_column(u'smyt_roomsmodel', 'department')

        # Deleting field 'RoomsModel.spots'
        db.delete_column(u'smyt_roomsmodel', 'spots')


        # User chose to not deal with backwards NULL issues for 'LanguagesModel.name'
        raise RuntimeError("Cannot reverse this migration. 'LanguagesModel.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'LanguagesModel.name'
        db.add_column(u'smyt_languagesmodel', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=20),
                      keep_default=False)

        # Deleting field 'LanguagesModel.department'
        db.delete_column(u'smyt_languagesmodel', 'department')

        # Deleting field 'LanguagesModel.spots'
        db.delete_column(u'smyt_languagesmodel', 'spots')

        # Deleting field 'UsersModel.paycheck'
        db.delete_column(u'smyt_usersmodel', 'paycheck')

        # Deleting field 'UsersModel.date_joined'
        db.delete_column(u'smyt_usersmodel', 'date_joined')


    models = {
        u'smyt.languagesmodel': {
            'Meta': {'object_name': 'LanguagesModel'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'smyt.roomsmodel': {
            'Meta': {'object_name': 'RoomsModel'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'smyt.usersmodel': {
            'Meta': {'object_name': 'UsersModel'},
            'date_joined': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'paycheck': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['smyt']