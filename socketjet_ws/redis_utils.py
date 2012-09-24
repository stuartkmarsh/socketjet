import redis
import threading   
import json    
from time import sleep 

import settings

CLIENTS = {}
REDIS_THREADS = {} 

def redis_connect(db=0):
    return redis.StrictRedis(host=settings.REDIS_HOST, db=db, password=settings.REDIS_PASSWORD)

def redis_monitor():          
    for k, v in REDIS_THREADS.iteritems():
        if not v.is_alive():
            redis_thread = threading.Thread(target=redis_listener, args=(k,)) 
            redis_thread.daemon = True
            redis_thread.start()                                           
            REDIS_THREADS[k] = redis_thread    
            

def redis_listener(api_key):
    '''
    Listens for incoming published messages on api_key channel name
    uses redis db=1 for transport
    '''
    
    while True:
        try:
            r = redis_connect(db=1)
            if r.ping():
                break
        except:
            pass 
                
    p = r.pubsub()
    p.subscribe(api_key)   
    
    try:
        for m in p.listen():
            data = json.loads(m['data'])
            action = data['action']
            
            if action == 'auth':
                key = data['api_key']
                conn_id = data['conn_id']
                channel = data['channel']  
                
                if CLIENTS[key]['conn_ids'].has_key(conn_id):
                    conn = CLIENTS[key]['conn_ids'][conn_id]

                    if channel.lower()[:7] == 'private':
                        CLIENTS[key]['event_auth'].setdefault(channel.lower(), set()).add(conn)
                        conn.is_authenticated = True
                        conn.emit('auth:%s' % channel, 'authenticated channel: %s' % channel)
                    else:                   
                        conn.is_authenticated = True
                        conn.emit('auth', 'authenticated')
                else:
                    continue
            elif action == 'emit' or action == 'broadcast':     
                channel = data['channel']
                message = data['message'] 
                conn_id = data['conn_id']
                
                if channel.lower()[:7] == 'private':
                    if CLIENTS[api_key]['event_auth'].has_key(channel.lower()):
                        conns = CLIENTS[api_key]['event_auth'][channel.lower()]
                elif channel.lower() == 'presence:joined':
                    conns = CLIENTS['api_key']['presence:joined']
                elif channel.lower() == 'presence:left':
                    conns = CLIENTS[api_key]['presence:left']     
                else:      
                    conns = CLIENTS[api_key]['subs'][channel]
                    
                for conn in conns:  
                    if action == 'broadcast':
                        if conn.conn_id == conn_id:
                            continue
                            
                    conn.emit(channel, message) 
            elif action == 'message':
                channel = data['channel']
                message = data['message']
                conn_id = data['conn_id']
                conn = CLIENTS[api_key]['conn_ids'][conn_id]
                conn.emit(channel, message)
                    
    except:
        pass
