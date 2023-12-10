import redis
import pika

while True:

    try:
        redis_conn = redis.Redis('redis-leader', 6379)
        redis_subscriber = redis_conn.pubsub()
        redis_subscriber.psubscribe('page:*:likes')
        rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
        rabbitmq_channel = rabbitmq_conn.channel()
        rabbitmq_channel.queue_declare(queue='likes-db-writer')

        for message in redis_subscriber.listen():
            if message['type'] == 'pmessage':
                channel = message['channel'].decode('utf-8')
                page_id = channel.split(':')[1]

                likes_count = int(message['data'].decode('utf-8'))

                rabbitmq_channel.basic_publish(
                    exchange='',  # default exchange, as we cannot publish directly to a queue in rabbitmq
                    routing_key='likes-db-writer',
                    body=f'{page_id}:{likes_count}'
                )

                print(f'Page {page_id} has {likes_count} likes', flush=True)

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
    