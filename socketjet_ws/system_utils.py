from redis_utils import CLIENTS
from tornado import database
import settings

def usage_update():
    '''
    updates the main db with connection and message numbers
    '''
    db = database.Connection(settings.DB_HOST, settings.DB_DATABASE, user=settings.DB_USER, 
                             password=settings.DB_PASSWORD)
                             
    for k, v in CLIENTS.iteritems():
        msgs = v['usage']['messages']
        conns = v['usage']['connections']
        if msgs == 0:
            continue
            
        v['usage']['messages'] = 0
        
        api_account = db.get('select id from common_apiaccount where api_key="%s"' % k)
        if api_account:
            db.execute('insert into common_usagetransaction (api_account_id, created, messages, connections) \
                   values (%s, NOW(), %s, %s)' % (api_account['id'], msgs, conns))
                   
    db.close()