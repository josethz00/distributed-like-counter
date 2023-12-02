import socket
import random
import redis

def is_write_operation(command):
    write_ops = ['set', 'del', 'lpush', 'incr', 'decr']
    return any(op in command.lower() for op in write_ops)

def process_request(client_socket, redis_connections):
    while True:
        command = client_socket.recv(1024).decode('utf-8')

        if not command:
            break

        if is_write_operation(command):
            response = redis_connections['leader'].execute_command(command)
        else:
            follower = random.choice(redis_connections['followers'])
            response = follower.execute_command(command)

        client_socket.send(response)

def start_proxy_server(host, port, redis_leader, redis_followers):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)

    redis_connections = {
        'leader': redis.Redis(host=redis_leader, port=6379),
        'followers': [redis.Redis(host=h, port=6379) for h in redis_followers]
    }

    print(f"Redis proxy running on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        process_request(client_socket, redis_connections)

if __name__ == "__main__":
    REDIS_LEADER = 'redis-leader'
    REDIS_FOLLOWERS = ['redis-follower-1', 'redis-follower-2', 'redis-follower-3']
    start_proxy_server('0.0.0.0', 6379, REDIS_LEADER, REDIS_FOLLOWERS)

