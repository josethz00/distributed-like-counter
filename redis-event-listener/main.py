import redis

redis_conn = redis.Redis('redis-leader', 6379)
redis_subscriber = redis_conn.pubsub()
redis_subscriber.psubscribe('page:*:likes')

for message in redis_subscriber.listen():
    with open('log.txt', 'a') as f:
        f.write(str(message))
    if message['type'] == 'pmessage':
        page_id = message['channel'].split(':')[1]
        likes_count = redis_conn.get(f'page:{page_id}:likes')
        print(f'Page {page_id} has {likes_count} likes', flush=True)
