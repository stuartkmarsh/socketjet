import pika 
import settings

def run():
    creds = pika.PlainCredentials(settings.RABBIT_USER, settings.RABBIT_PASS)
    parms = pika.ConnectionParameters(credentials=creds, host=settings.RABBIT_HOST)
    conn = pika.BlockingConnection(parms)

    channel = conn.channel()
    channel.queue_declare(queue='server_post', durable=True, exclusive=False, auto_delete=False)

    def callback(ch, method, properties, body):
        print 'received: %s' % body
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='server_post')

    channel.start_consuming() 
    
if __name__ == '__main__':
    run()
      