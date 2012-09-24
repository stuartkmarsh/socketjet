# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AccountPackage'
        db.create_table('common_accountpackage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('max_connections', self.gf('django.db.models.fields.IntegerField')()),
            ('max_messages', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('common', ['AccountPackage'])

        # Adding model 'AccountUserProfile'
        db.create_table('common_accountuserprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('current_monthly_messages', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('account_package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.AccountPackage'])),
        ))
        db.send_create_signal('common', ['AccountUserProfile'])

        # Adding field 'ApiAccount.site_prefix'
        db.add_column('common_apiaccount', 'site_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)

        # Deleting field 'UserProfile.max_messages'
        db.delete_column('common_userprofile', 'max_messages')

        # Deleting field 'UserProfile.current_monthly_messages'
        db.delete_column('common_userprofile', 'current_monthly_messages')

        # Deleting field 'UserProfile.max_connections'
        db.delete_column('common_userprofile', 'max_connections')

        # Adding field 'UserProfile.api_account'
        db.add_column('common_userprofile', 'api_account', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['common.ApiAccount']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'AccountPackage'
        db.delete_table('common_accountpackage')

        # Deleting model 'AccountUserProfile'
        db.delete_table('common_accountuserprofile')

        # Deleting field 'ApiAccount.site_prefix'
        db.delete_column('common_apiaccount', 'site_prefix')

        # User chose to not deal with backwards NULL issues for 'UserProfile.max_messages'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.max_messages' and its values cannot be restored.")

        # Adding field 'UserProfile.current_monthly_messages'
        db.add_column('common_userprofile', 'current_monthly_messages', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'UserProfile.max_connections'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.max_connections' and its values cannot be restored.")

        # Deleting field 'UserProfile.api_account'
        db.delete_column('common_userprofile', 'api_account_id')


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
        'common.accountpackage': {
            'Meta': {'object_name': 'AccountPackage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_connections': ('django.db.models.fields.IntegerField', [], {}),
            'max_messages': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'common.accountuserprofile': {
            'Meta': {'object_name': 'AccountUserProfile'},
            'account_package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.AccountPackage']"}),
            'current_monthly_messages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
            'site_prefix': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.clientuserpermissions': {
            'Meta': {'object_name': 'ClientUserPermissions'},
            'api_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ApiAccount']"}),
            'client_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'db_del': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'api_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ApiAccount']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
