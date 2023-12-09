import redis

redis_conn = redis.Redis('redis-leader', 6379)
redis_subscriber = redis_conn.pubsub()
redis_subscriber.psubscribe('page:*:likes')

for message in redis_subscriber.listen():
    if message['type'] == 'pmessage':
        channel = message['channel'].decode('utf-8')
        page_id = channel.split(':')[1]

        likes_count = int(message['data'].decode('utf-8'))
        print(f'Page {page_id} has {likes_count} likes', flush=True)
