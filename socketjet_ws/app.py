from os import path as op
import sys  

import tornado 
from tornado import database, ioloop
import tornadio2
from tornadio2.conn import event
import redis 
import json 
import threading
import time  
from MySQLdb import connect

from redis_utils import redis_monitor, redis_listener, redis_connect, CLIENTS, REDIS_THREADS
from rabbitmq_utils import server_post, CallbackNotDefined 
from system_utils import usage_update
import settings

ROOT = op.normpath(op.dirname(__file__)) 

REQUIRE_AUTH = ['send-data',
                'db-set',
                'db-get']    
                
def log(message):
    fp = open('ws.log', 'a')
    fp.write('%s\n' % message)
    fp.close()
         
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class SocketIOHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('socket_lib/socket.io.js')  
   
class WSConnection(tornadio2.SocketConnection):                 
    def on_open(self, request):    
        log('ws connecting')
        self.api_key = request.get_argument('api_key') 
        self.user_id = request.get_argument('user_id')     
        self.is_authenticated = False
        
        # get conn id    
        r = redis_connect(db=1)
        self.conn_id = str(r.incr('conn_id'))    

        CLIENTS.setdefault(self.api_key, {})   
        
        client = CLIENTS[self.api_key]
        client.setdefault('conns', set()).add(self)
        client.setdefault('event_auth', {})
        client.setdefault('subs', {})
        client.setdefault('presence:joined', set())
        client.setdefault('presence:left', set()) 
        client.setdefault('usage', {})
        client.setdefault('conn_ids', {})
        client['conn_ids'][self.conn_id] = self
        client['usage'].setdefault('messages', 0)
        client['usage'].setdefault('connections', 0)
        client['usage']['connections'] += 1

        # check api_key exists in db 
        try:
            db = database.Connection(settings.DB_HOST, settings.DB_DATABASE, user=settings.DB_USER, password=settings.DB_PASSWORD)
            api_result = db.get('SELECT id, callback_url, disabled from common_apiaccount where api_key="%s"' % self.api_key)
            db.close()
            if api_result:
                if api_result['disabled'] == 1:
                    return False
                    
                self.callback_url = api_result['callback_url']         
            else:
                return False     
        except:
            return False       

        # start a redis listener thread for this api_key
        if not REDIS_THREADS.has_key(self.api_key):
            redis_thread = threading.Thread(target=redis_listener, args=(self.api_key,))
            redis_thread.daemon = True  
            REDIS_THREADS[self.api_key] = redis_thread 
            redis_thread.start()
            
        # emit presence event (broadcast)       
        r = redis_connect()     
        r.publish(self.api_key, json.dumps({'action':'broadcast',
                                            'api_key':self.api_key,
                                            'conn_id':self.conn_id,
                                            'channel':'presence:joined',
                                            'message':json.dumps({'conn_id':self.conn_id, 'user_id':self.user_id})}))   
        self.add_msg_count() 
        
        return self.conn_id  
        
    def on_message(self, message):
        print message
        
    def on_event(self, name, *args, **kwargs):
        '''
        set, get and del channel names are reserved name for redis persistence
        send_data name is reserved for sending to the users server 
        sub and unsub are reserved for subscribing and unsubscribing to an event
        if the name starts with `private` it only gets emitted to authenticated members
        '''         
        self.add_msg_count() # for the incoming message  
        name = name.lower()
        
        if name in REQUIRE_AUTH:
            if not self.is_authenticated:
                return 'not authenticated'
        
        if args:
            arg0 = args[0].lower()
            
        '''
        get-connid returns connection id
        '''
        if name == 'get-connid':
            return self.conn_id
            
        '''
        send data to callback address
        adds message to the queue
        js usage: socket.emit('send-data', 'mydata');
        returns error msg if no callback is defined on the api account 
        ***** future feature *****
              
        if name == 'send-data':
            try:
                server_post(self, arg0)
                self.emit(name, 'success')
            except CallbackNotDefined:
                self.emit(name, 'callback not defined')
            except:                    
                self.emit(name, 'error')
            
            self.add_msg_count()    
            return
        '''
            
        '''
        get data from key value store
        returns value for the key provided
        js usage: socket.emit('db-get', 'foo');
        '''     
        if name == 'db-get': 
            try:                 
                r = redis_connect()
                self.emit(name, r.get('%s:%s' % (self.api_key, arg0)))  
            except:
                self.emit(name, 'error')
                          
            self.add_msg_count()
            return
            
        '''
        sets data on the key value store
        can set multiple keys
        js usage: socket.emit('db-set', {foo:'bar', bash:'bosh'});
        '''                
        if name == 'db-set':
            try:    
                r = redis_connect()
                results = {}
                for k, v in kwargs.iteritems():
                    res = r.set('%s:%s' % (self.api_key, k), v)
                    results[k] = res          
                    
                self.emit(name, json.dumps(results))
            except:
                self.emit(name, 'error')
            
            self.add_msg_count()
            return 
        
        '''
        deletes a key from the key value store
        js usage: socket.emit('db-del', 'mykey');
        **** future feature, or will not implement        
        if name == 'db-del':
            try:
                r = redis_connect()
                res = r.delete('%s:%s' % (self.api_key, arg0))
                self.emit(name, json.dumps({arg0:res}))    
            except:
                self.emit(name, 'error')
            
            self.add_msg_count()
            return 
        '''    
                  
        '''
        if name starts with 'private' message is emitted to authorised subscribers
        can set broadcast with {broadcast:true}
        js usage: socket.emit('private-chan', {message:'hello'});
        '''    
        if name[:7] == 'private':
            if CLIENTS[self.api_key]['event_auth'].has_key(name):
                conns = CLIENTS[self.api_key]['event_auth'][name]   
                
                if not self in conns:
                    return 'not authorized'
                    
                r = redis_connect() 
                
                action = 'emit' 
                if kwargs.get('broadcast', False):
                    action = 'broadcast'      
                    
                r.publish(self.api_key, json.dumps({'action':action,
                                                    'api_key':self.api_key,
                                                    'conn_id':self.conn_id,
                                                    'channel':name,
                                                    'message':kwargs['message']}))
                
                self.add_msg_count()    
                return 
                    
            return 'not authenticated'
            
        # sub/unsub 
        '''
        subscribe/unsubscribe to a channel
        if event is 'presence:joined' or 'presence:left' then user is subscribed
        to those special events.
        js usage: socket.emit('subscribe', 'mychannel');
        '''
        subs = CLIENTS[self.api_key]['subs'] 
        presence_joined = CLIENTS[self.api_key]['presence:joined']
        presence_left = CLIENTS[self.api_key]['presence:left']
            
        if name == 'subscribe':
            event = arg0
            if event == 'presence:joined':
                presence_joined.add(self)    
            elif event == 'presence:left':
                presence_left.add(self)              
            else:
                subs.setdefault(event, set()).add(self)
            
            self.add_msg_count()   
            return 'subscribed'
            
        if name == 'unsubscribe':
            event = arg0       
            self.add_msg_count()
            if event == 'presence:joined':
                try:
                    presence_joined.remove(self)
                    return 'unsubscribed'
                except:
                    return 'not subscribed'
            elif event == 'presence:left':
                try:
                    presence_left.remove(self)
                    return 'unsubscribed'
                except:
                    return 'not subscribed'
                    
            if event in subs:
                if self in subs[event]:
                    subs[event].remove(self)     
                    return 'unsubscribed'
            return 'not subscribed'
        
        '''
        emits a message to all subscribed clients
        if kwarg 'broadcast' exists and is True, doesn't send to caller
        '''        
        if not self.is_authenticated:   
            return 'not authenticated'
            
        if subs.has_key(name):  
            r = redis_connect() 
            
            action = 'emit' 
            if kwargs.get('broadcast', False):
                action = 'broadcast'      
                            
            r.publish(self.api_key, json.dumps({'action':action,
                                                'api_key':self.api_key,
                                                'conn_id':self.conn_id,
                                                'channel':name,
                                                'message':kwargs['message']}))
            
            self.add_msg_count()
        
        
    def on_close(self):
        if not CLIENTS[self.api_key]['usage']['connections'] == 0:
            CLIENTS[self.api_key]['usage']['connections'] -= 1 
            
        # emit presence event (broadcast)
        r = redis_connect()     
        r.publish(self.api_key, json.dumps({'action':'broadcast',
                                            'api_key':self.api_key,
                                            'conn_id':self.conn_id,
                                            'channel':'presence:left',
                                            'message':json.dumps({'conn_id':self.conn_id, 'user_id':self.user_id})}))   
        self.add_msg_count()
            
    def add_msg_count(self):
        CLIENTS[self.api_key]['usage']['messages'] += 1                                      

MyRouter = tornadio2.TornadioRouter(WSConnection)


if __name__ == '__main__':
    try:
        port = sys.argv[1]
        print 'starting server on port %s' % port
        io_loop = ioloop.IOLoop.instance()
    
        # add redis monitor loop
        redis_loop = ioloop.PeriodicCallback(redis_monitor, 1000, io_loop=io_loop)
        redis_loop.start()      
    
        # add usage monitor loop
        usage_loop = ioloop.PeriodicCallback(usage_update, 30000, io_loop=io_loop)
        usage_loop.start()
        
        application = tornado.web.Application(             
            MyRouter.urls,
            socket_io_port = port,                              
        )
        
        socketio_server = tornadio2.server.SocketServer(application, io_loop=io_loop)
    except IndexError:
        print 'please pass the port number' 
        
    
