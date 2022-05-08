import redis
from hotqueue import HotQueue

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = redis.Redis(host=redis_ip, port=6379, db=0)
q = HotQueue("queue", host=redis_ip, port=6379, db=1)
job_db = redis.Redis(host=redis_ip, port=6379, db=2, decode_responses=True)


