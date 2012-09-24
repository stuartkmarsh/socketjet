import pika
import settings
import json

class CallbackNotDefined(Exception): pass

def server_post(ws_obj, message):
    if ws_obj.callback_url:     
        creds = pika.PlainCredentials(settings.RABBIT_USER, settings.RABBIT_PASS)
        parms = pika.ConnectionParameters(credentials=creds, host=settings.RABBIT_HOST)
        conn = pika.BlockingConnection(parms)
    
        channel = conn.channel()
        channel.queue_declare(queue='server_post', durable=True, exclusive=False, auto_delete=False)
        channel.basic_publish(exchange='', routing_key='server_post', 
                              body=json.dumps((ws_obj.api_key,message)),
                              properties=pika.BasicProperties(delivery_mode=2))    
                          
        conn.close()
    else:
        raise CallbackNotDefined