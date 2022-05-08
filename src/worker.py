from jobs import q, update_job_status
import time

@q.worker
def execute_job(job_id):
    update_job_status(job_id, 'in progress')
    time.sleep(15)
    update_job_status(job_id, 'complete')

execute_job()
