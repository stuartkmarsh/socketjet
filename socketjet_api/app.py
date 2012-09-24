import tornado.ioloop
import tornado.web 
from tornado import database

import hmac
import hashlib 
import settings 
import redis 
import json    
import sys

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        channel = self.get_argument('channel', None) # optional
        api_key = self.get_argument('api_key', None)
        conn_id = self.get_argument('conn_id', None)
        action = self.get_argument('action', None)
        message = self.get_argument('message', None)
        data = self.get_argument('data', None)
        
        if not api_key or not conn_id or not data or not action:
            self.send_error(status_code=403)
        else:
            # get secret key for api account
            db = database.Connection(settings.DB_HOST, settings.DB_DATABASE, user=settings.DB_USER, password=settings.DB_PASSWORD)
            api_result = db.get('SELECT secret_key from common_apiaccount where api_key="%s"' % api_key)
            db.close()

            if api_result:
                secret = str(api_result['secret_key'])
                local_data = '%s:%s' % (conn_id, api_key)
                local_data = hmac.new(secret, msg=local_data, digestmod=hashlib.sha256).hexdigest()
                if local_data == data:
                    r = redis.StrictRedis(host=settings.REDIS_HOST, db=1, password=settings.REDIS_PASSWORD)
                    r.publish(api_key, json.dumps({'action':action,
                                                   'api_key':api_key,
                                                   'conn_id':conn_id, 
                                                   'channel':channel,
                                                   'message':message
                                                   })) 
                    

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/socket_push/", MainHandler)
    ])           
    
    if len(sys.argv) == 2:
        port = sys.argv[1]
    else:
        port = 8002
        
    application.listen(port) 
    print 'Start api server on port %s' % port
    tornado.ioloop.IOLoop.instance().start()
