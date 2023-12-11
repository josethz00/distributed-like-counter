import pika
import psycopg2

pg_conn = psycopg2.connect(
    database="likesdb",
    user="likesdb",
    password="likesdb",
    host="postgres-db",
    port=5432
)

while True:
    try:

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
        channel = connection.channel()

        channel.queue_declare(queue='likes-db-writer')

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            page_id, likes_count = body.decode('utf-8').split(':')
            cur = pg_conn.cursor()
            cur.execute("UPDATE likes SET likes_count = %s WHERE page_id = %s", (likes_count, page_id))
            cur.close()
            ch.basic_ack(delivery_tag = method.delivery_tag)

        # QOS — Quality of Service
        channel.basic_qos(prefetch_count=1)  # process one message at once, won't pull more if not done with processing
        channel.basic_consume(queue='likes-db-writer', 
        on_message_callback=callback)

        print(' [*] Waiting for messages.')
        channel.start_consuming()

    # Do not recover if connection was closed by broker
    except pika.exceptions.ConnectionClosedByBroker:
        break
    # Do not recover on channel errors
    except pika.exceptions.AMQPChannelError:
        break
    # Recover on all other connection errors
    except pika.exceptions.AMQPConnectionError:
        # other exceptions such as StreamLostError and TimeoutError
        # inherit from AMQPConnectionError
        continue
    