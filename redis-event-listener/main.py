import redis

redis_conn = redis.Redis('redis-leader', 6379)
redis_subscriber = redis_conn.pubsub()
redis_subscriber.psubscribe('page:*:likes')

for message in redis_subscriber.listen():
    if message['type'] == 'pmessage':
        channel = message['channel'].decode('utf-8')
        page_id = channel.split(':')[1]

        print(message['data'], flush=True)

        likes_count = redis_conn.get(f'page:{page_id}:likes')
        if likes_count:
            likes_count = likes_count.decode('utf-8')
        print(f'Page {page_id} has {likes_count} likes', flush=True)
