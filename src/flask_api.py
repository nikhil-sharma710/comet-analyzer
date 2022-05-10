from flask import Flask, jsonify, request, send_file
import logging
import json
import redis
import os
from jobs import rd, q, add_job, get_job_by_id, jdb, hdb
from uuid import uuid4

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/read-data', methods=['POST', 'GET', 'DELETE'])
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
            rd.hset(str(uuid4()), mapping=item)

        return f'Data has been loaded to Redis from file\n'

    elif request.method == 'GET':
        comet_empty_list = []
        for item in rd.keys():
            comet_empty_list.append(rd.hgetall(item))

        return json.dumps(comet_empty_list, indent=2)

    elif request.method == 'DELETE':
        rd.flushdb()
        return 'All data in redis container db = 0 has been deleted\n'


@app.route('/info', methods=['GET'])
def info():

    """
    Informational
    """

    return """
  Try the following routes:
  /info                  				GET      informational
  /read-data             				POST     read data into redis database
                         				GET      show list of comets data
                         				DELETE   delete existing data from database

  /symbols               				GET      info on what each symbol means

  /comets                				GET      display list of comet names and their respective ID's
  /comets/<comet_id>     				GET      display info about specific comet
  /comets/delete/<comet_id>     			DELETE   delete data on specific comet
  /comets/update/<comet_id>/<key_value/<new_value       PUT      update/change a specific piece of info on specific comet
   
  /jobs                  				GET      info on how to submit job
                        				POST     submit job

  /jobs/<jobid>          				GET      info on job
  /list-of-jobs          				GET      list of all the jobs


"""

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

        return json.dumps(add_job(job['min_au'], job['max_au'], job['num_bins']), indent=2) + '\n'

    elif request.method == 'GET':
        return """
  To submit a job, do the following:
  curl localhost:5014/jobs -X POST -d '{"min_au": "<minimum AU value>", "max_au": "<maximum AU value>", "num_bins": "<number of bins>"}' -H "Content-Type: application/json"

"""

@app.route('/list-of-jobs', methods=['GET'])
def get_list_of_jobs():
    """

    """

    logging.info('Querying route to get all comets')

    job_list = []
    for item in jdb.keys():
        job_list.append(jdb.hgetall(item))

    return json.dumps(job_list, indent=2)

@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid):
    """
    API route for checking on the status of a submitted job
    """

    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'


@app.route('/download/<jobid>', methods=['GET'])
def download(jobid):
    path = f'/app/{jobid}.png'
    with open(path, 'wb') as f:
        f.write(hdb.get(jobid))
    return send_file(path, mimetype='image/png', as_attachment=True)


@app.route('/comets/delete/<comet_id>', methods=['DELETE'])
def delete_specific_comet(comet_id):
    """

    """

    comet_name = rd.hget(comet_id, "object")

    rd.delete(comet_id)

    return f'Deleted {comet_name}\n'


@app.route('/symbols', methods=['GET'])
def get_symbols():
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
        comets_names.append(str(item) + " - " + rd.hget(item, 'object'))

    return json.dumps(comets_names, indent=2)


@app.route('/comets/<comet_id>', methods=['GET'])
def get_specific_comet(comet_id):
    """

    """

    return json.dumps(rd.hgetall(comet_id), indent=2)


@app.route('/comets/update/<comet_id>/<key_value>/<new_value>', methods=['PUT'])
def update_key_value(comet_id, key_value, new_value):
    """

    """

    rd.hset(comet_id, key_value, new_value)

    return f'Updated {key_value} to {new_value} in {rd.hget(comet_id, "object")}\n'




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
