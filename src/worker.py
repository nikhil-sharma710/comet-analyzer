from jobs import rd, q, add_job, get_job_by_id, jdb
import time
import matplotlib as plt
import numpy as np
import redis
import os

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

hdb = redis.StrictRedis(host=redis_ip, port=6379, db=3)

@q.worker
def execute_job(jid):
    update_job_status(jid, 'started')

    data = jdb.hgetall(jid)

    min_au_value = data['min_au']
    max_au_value = data['max_au']
    n = data['num_bins']

    list_of_values = []

    for item in rd.keys():
        if rd.hget(item, 'q_au_2') >= min_au_value and rd.hget(item, 'q_au_2') <= max_au_value:
            list_of_values.append(rd.hget(item, 'q_au_2'))

    plt.hist(list_of_values, n)
    plt.xlabel('Aphelion Distance, in AU')
    plt.ylabel('Frequency')
    plt.title('Histogram of Aphelion Distance')
    plt.savefig('histogram.png')
    plt.show()
 
    file_bytes = open('/tmp/histogram.png', 'rb').read()

    hdb.set('key', file_bytes)

    time.sleep(15)
    update_job_status(jid, 'finished')

execute_job()
