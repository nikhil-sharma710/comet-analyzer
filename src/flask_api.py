from flask import Flask, jsonify, request
import logging
import json
import redis
import os
from jobs import rd, q, add_job, get_job_by_id

logging.basicConfig(level=logging.DEBUG)

#redis_ip = os.environ.get('REDIS_IP')
#if not redis_ip:
#    raise Exception()

app = Flask(__name__)
#rd = redis.Redis(host=redis_ip, port=6379, db=0)

# comets_data = {}


@app.route('/read_data', methods=['POST', 'GET'])
def read_data_from_file():
    """
    
    """

    logging.info('Reading data...')

    global comets_data

    if request.method == 'POST':

        rd.flushdb()

        with open('comets_data.json', 'r') as f:
            comets_data = json.load(f)

        for item in comets_data:
            rd.hset(item['object'], json.dumps(item))

        return f'Data has been read from file\n'

    elif request.method == 'GET':
        comet_empty_list = []
        for item in rd.keys():
            comet_empty_list.append(json.loads(rd.hget(item).decode('utf-8')))
  
        return json.dumps(comet_empty_list, indent=2)

    elif request.method == 'DELETE':
        rd.flushdb()
        return 'All data in redis container db = 0 has been deleted\n'

@app.route('/jobs', methods=['POST', 'GET'])
def jobs_api():
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created.
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['start'], job['end']), indent=2) + '\n'

    elif request.method == 'GET':
        return """
  To submit a job, do the following:
  curl localhost:5041/jobs -X POST -d '{"start":1, "end":2}' -H "Content-Type: application/json"
"""

        

@app.route('/symbols', methods=['GET'])
def info():
    """

    """

    logging.info('Showing what each symbol means')

    describe = "\n" 
    describe += "Symbols:    Description:\n"
    describe += "TP          time of perihelion passage, in TDB; this is the time when the comet was closest to the Sun\n"
    describe += "e           the orbital eccentricity of the comet\n"
    describe += "i           Inclination of the orbit with respect to the ecliptic plane and the equinox of J2000 (J2000-Ecliptic), in degrees\n"
    describe += "w           Argument of perihelion (J2000-Ecliptic), in degrees\n"
    describe += "Node        Longitude of the ascending node (J2000-Ecliptic), in degrees\n"
    describe += "q           comet's distance at perihelion, in AU\n"
    describe += "Q           comet's distance at aphelion, in AU\n"
    describe += "P           orbital period, in Julian years\n"
    describe += "A1          Non-gravitational force parameter A1\n"
    describe += "A2          Non-gravitational force parameter A2\n"
    describe += "A3          Non-gravitational force parameter A3\n"
    describe += "MOID(AU)    Minimum orbit intersection distance (the minimum distance between the osculating orbits of the NEO and the Earth)\n"
    describe += "ref         Orbital solution reference\n\n"

    return describe


	
@app.route('/comets', methods=['GET'])
def get_comets():
    """

    """

    logging.info('Querying route to get all comets')

    comets_names = []
    for item in rd.keys():
        comets_names.append(json.loads(rd.get(item, 'object')))

    return json.dumps(comets_names, indent=2)



@app.route('/aphelion/<au>', methods=['GET'])
def far_comets(au: int):
    """
    returns comets above some given distance in AU units
    """

    aph_list = []
    for item in rd.keys():
        if float(rd.hget(item, 'q_au_2')) >= float(au):
            aph_list.append('[Object ' + json.loads(rd.hget(item, 'object')) + ']: ', rd.hget(item, 'q_au_2'))
    
    return(f'Comets having distance greater than {au}\n' + json.dumps(aph_list, indent=2) + '\n')



@app.route('/test', methods=['GET'])
def testing():

    needed_data = ['object', 'epoch_tdb', 'tp_tdb', 'e', 'i_deg', 'w_deg', 'node_deg', 'q_au_1', 'q_au_2', 'p_yr', 'moid_au', 'ref', 'object_name']
    empty_dict = {}
    for item in comets_data:
        if 'P/2004 R1 (McNaught)' == item['object']:    
            for data in needed_data:
                empty_dict[data] = item[data]

    return empty_dict

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
