# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Domain'
        db.create_table('common_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('common', ['Domain'])

        # Adding model 'ApiAccount'
        db.create_table('common_apiaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_key', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['ApiAccount'])

        # Adding M2M table for field domains on 'ApiAccount'
        db.create_table('common_apiaccount_domains', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('apiaccount', models.ForeignKey(orm['common.apiaccount'], null=False)),
            ('domain', models.ForeignKey(orm['common.domain'], null=False))
        ))
        db.create_unique('common_apiaccount_domains', ['apiaccount_id', 'domain_id'])

        # Adding model 'UserProfile'
        db.create_table('common_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('account_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('max_connections', self.gf('django.db.models.fields.IntegerField')()),
            ('max_messages', self.gf('django.db.models.fields.IntegerField')()),
            ('current_monthly_messages', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('common', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Domain'
        db.delete_table('common_domain')

        # Deleting model 'ApiAccount'
        db.delete_table('common_apiaccount')

        # Removing M2M table for field domains on 'ApiAccount'
        db.delete_table('common_apiaccount_domains')

        # Deleting model 'UserProfile'
        db.delete_table('common_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.apiaccount': {
            'Meta': {'object_name': 'ApiAccount'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domains': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Domain']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.domain': {
            'Meta': {'object_name': 'Domain'},
            'domain': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_monthly_messages': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_connections': ('django.db.models.fields.IntegerField', [], {}),
            'max_messages': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']
