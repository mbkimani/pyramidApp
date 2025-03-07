from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import redis.cluster

# Create Redis cluster client as a global instance
redis_client = redis.cluster.RedisCluster(
    host='clustercfg.test-cluster.fcagwe.euw2.cache.amazonaws.com',
    port=6379,
    ssl=True
)

def hello_world(request):
    return Response('Hello, World!')

def set_redis_value(request):
    try:
        # Set value in Redis
        redis_client.set("key", "value")
        return Response('Value set in Redis successfully')
    except Exception as e:
        return Response(f'Error setting Redis value: {str(e)}', status=500)

def get_redis_value(request):
    try:
        # Get value from Redis
        value = redis_client.get("key")
        if value:
            return Response(f'Value from Redis: {value.decode()}')
        return Response('No value found', status=404)
    except Exception as e:
        return Response(f'Error getting Redis value: {str(e)}', status=500)

if __name__ == '__main__':
    try:
        with Configurator() as config:
            # Add routes
            config.add_route('hello', '/')
            config.add_route('set_redis', '/set')
            config.add_route('get_redis', '/get')

            # Add views
            config.add_view(hello_world, route_name='hello')
            config.add_view(set_redis_value, route_name='set_redis')
            config.add_view(get_redis_value, route_name='get_redis')

            app = config.make_wsgi_app()

        server = make_server('0.0.0.0', 8080, app)
        print('Web server started on http://0.0.0.0:8080')
        server.serve_forever()

    finally:
        # Ensure Redis connection is closed when the server stops
        redis_client.close()

