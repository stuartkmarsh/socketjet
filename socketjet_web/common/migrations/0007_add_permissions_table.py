# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ClientUserPermissions'
        db.create_table('common_clientuserpermissions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('api_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.ApiAccount'])),
            ('db_del', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('common', ['ClientUserPermissions'])

        # Adding M2M table for field private_channels on 'ClientUserPermissions'
        db.create_table('common_clientuserpermissions_private_channels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clientuserpermissions', models.ForeignKey(orm['common.clientuserpermissions'], null=False)),
            ('usercreatedchannel', models.ForeignKey(orm['common.usercreatedchannel'], null=False))
        ))
        db.create_unique('common_clientuserpermissions_private_channels', ['clientuserpermissions_id', 'usercreatedchannel_id'])

        # Adding model 'UserCreatedChannel'
        db.create_table('common_usercreatedchannel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('common', ['UserCreatedChannel'])

        # Adding field 'ApiAccount.nickname'
        db.add_column('common_apiaccount', 'nickname', self.gf('django.db.models.fields.CharField')(default='user 1', max_length=50), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'ClientUserPermissions'
        db.delete_table('common_clientuserpermissions')

        # Removing M2M table for field private_channels on 'ClientUserPermissions'
        db.delete_table('common_clientuserpermissions_private_channels')

        # Deleting model 'UserCreatedChannel'
        db.delete_table('common_usercreatedchannel')

        # Deleting field 'ApiAccount.nickname'
        db.delete_column('common_apiaccount', 'nickname')


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
            'callback_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'secret_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.clientuserpermissions': {
            'Meta': {'object_name': 'ClientUserPermissions'},
            'api_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ApiAccount']"}),
            'client_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'db_del': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'private_channels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['common.UserCreatedChannel']", 'null': 'True', 'blank': 'True'})
        },
        'common.usagetransaction': {
            'Meta': {'object_name': 'UsageTransaction'},
            'api_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ApiAccount']"}),
            'connections': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'common.usercreatedchannel': {
            'Meta': {'object_name': 'UserCreatedChannel'},
            'channel_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_monthly_messages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
