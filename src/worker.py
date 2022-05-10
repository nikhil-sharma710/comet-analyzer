from jobs import rd, q, jdb, hdb, add_job, get_job_by_id, update_job_status
import time
import matplotlib.pyplot as plt
import os

@q.worker
def execute_job(jid):
    update_job_status(jid, 'started')
    time.sleep(5)

    data = jdb.hgetall(f'job.{jid}')

    min_au_value = data['min_au']
    max_au_value = data['max_au']
    n = int(data['num_bins'])

    list_of_values = []

    for item in rd.keys():
        if rd.hget(item, 'q_au_2') >= min_au_value and rd.hget(item, 'q_au_2') <= max_au_value:
            list_of_values.append(rd.hget(item, 'q_au_2'))

    plt.hist(list_of_values, n)
    plt.xlabel('Aphelion Distance, in AU')
    plt.xlim(min_au_value, max_au_value)
    plt.ylabel('Frequency')
    plt.ylim(0, 50)
    plt.title('Histogram of Aphelion Distance')
    plt.savefig('histogram.png')
 
    file_bytes = open('histogram.png', 'rb').read()

    hdb.set(jid, file_bytes)

    update_job_status(jid, 'finished')

execute_job()
