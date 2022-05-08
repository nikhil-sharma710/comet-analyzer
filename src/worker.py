import redis
from hotqueue import HotQueue

redis_ip = os.environ.get('REDIS_IP')

rd = redis.Redis(host=redis_ip, port=6379, db=0)
q = HotQueue("queue", host=redis_ip, port=6379, db=1)
