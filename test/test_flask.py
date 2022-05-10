import json
import os
import re
import time

import pytest
import requests


api_host = 'localhost'
api_port = '5014'
api_prefix = f'http://{api_host}:{api_port}'


def test_info():
    route = f'{api_prefix}/info'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('Try the following routes', response.text)) == True


def test_read_data_from_file():
    route = f'{api_prefix}/read-data'
    response = requests.post(route)

    assert response.ok == True
    assert response.status_code == 200
    assert response.content == b'Data has been loaded to Redis from file\n'


def test_get_comets():
    route = f'{api_prefix}/read-data'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    assert isinstance(response.json(), list) == True
    assert isinstance(response.json()[0], dict) == True
    assert 'object' in response.json()[0].keys()
    assert 'epoch_tdb' in response.json()[0].keys()
    assert 'tp_tdb' in response.json()[0].keys()
    assert 'e' in response.json()[0].keys()
    assert 'i_deg' in response.json()[0].keys()
    assert 'w_deg' in response.json()[0].keys()
    assert 'node_deg' in response.json()[0].keys()
    assert 'q_au_1' in response.json()[0].keys()
    assert 'q_au_2' in response.json()[0].keys()
    assert 'p_yr' in response.json()[0].keys()
    assert 'moid_au' in response.json()[0].keys()
    assert 'ref' in response.json()[0].keys()
    assert 'object_name' in response.json()[0].keys()

def test_jobs_api():
    route = f'{api_prefix}/jobs'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('To submit a job,', response.text)) == True


def test_jobs_cycle():
    route = f'{api_prefix}/jobs'
    job_data = {'min_au': 5, 'max_au': 10, 'num_bins': 3}
    response = requests.post(route, json=job_data)

    assert response.ok == True
    assert response.status_code == 200
    
    UUID = response.json()['id']
    assert isinstance(UUID, str) == True
    assert response.json()['status'] == 'submitted'
    assert int(response.json()['min_au']) == int(job_data['min_au'])
    assert int(response.json()['max_au']) == int(job_data['max_au'])
    assert int(response.json()['num_bins']) == int(job_data['num_bins'])

    time.sleep(1)
    route = f'{api_prefix}/jobs/{UUID}'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    assert response.json()['status'] == 'started'
    assert int(response.json()['min_au']) == int(job_data['min_au'])
    assert int(response.json()['max_au']) == int(job_data['max_au'])
    assert int(response.json()['num_bins']) == int(job_data['num_bins'])

    time.sleep(10)
    route = f'{api_prefix}/jobs/{UUID}'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    assert response.json()['status'] == 'finished'
    assert int(response.json()['min_au']) == int(job_data['min_au'])
    assert int(response.json()['max_au']) == int(job_data['max_au'])
    assert int(response.json()['num_bins']) == int(job_data['num_bins'])
