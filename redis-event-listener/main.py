import redis



redis_conn = redis.Redis('redis-leader', 6379)
redis_subscriber = redis_conn.pubsub().psubscribe('page:*:likes')

for message in redis_subscriber.listen():

    print('aaaa')
    if message['type'] == 'pmessage':
        page_id = message['channel'].split(':')[1]
        likes_count = redis_conn.get(f'page:{page_id}:likes')
        print(f'Page {page_id} has {likes_count} likes')
