import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='likes-db-writer')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

# QOS — Quality of Service
channel.basic_qos(prefetch_count=1)  # process one message at once, won't pull more if not done with processing
channel.basic_consume(callback,
                      queue='likes-db-writer')

print(' [*] Waiting for messages.')
channel.start_consuming()