from flask import Flask, jsonify, request
import logging
import json
import redis
import os

logging.basicConfig(level=logging.DEBUG)

redis_ip = os.environ.get('REDIS_IP')
app = Flask(__name__)
rd = redis.Redis(host=redis_ip, port=6379, db=0)

# comets_data = {}


@app.route('/read_data', methods=['POST', 'GET', 'PUT', 'DELETE'])
def read_data_from_file() -> str:
    """
    
    """

    logging.info('Reading data...')

    global comets_data

    if request.method == 'POST':
        with open('comets_data.json', 'r') as f:
            comets_data = json.load(f)

        for item in range(len(comets_data)):
            rd.set(str(i), json.dumps(comets_data[item]))

        return f'Data has been read from file\n'

    else:
        comet_empty_list = []
        for item in rd.keys():
            comet_empty_list.append(json.loads(rd.get(i).decode('utf-8')))
  
        return json.dumps(comet_empty_list, indent=2)


@app.route('/symbols', methods=['GET'])
def info() -> str:
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


@app.route('/display_data', methods=['GET'])
def display_data() -> str:
    """

    """

    logging.info('Querying route to display data')

    return json.dumps(comets_data, indent=2)


	
@app.route('/comets', methods=['GET'])
def get_comets() -> str:
    """

    """

    logging.info('Querying route to get all comets')

    comets_names = []
    for item in comets_data:
        comets_names.append(item['object'])

    return json.dumps(comets_names, indent=2)


@app.route('/comets/<comet>', methods=['GET'])
def get_comet_info(comet) -> str:
    """

    """

    logging.info('Querying route to get all info on /' + comet)

    comet_dict = {}
    comet_list = []
    comet_data = ['object', 'epoch_tdb', 'tp_tdb', 'e', 'i_deg', 'w_deg', 'node_deg', 'q_au_1', 'q_au_2', 'p_yr', 'moid_au', 'ref', 'object_name']

    for item in comets_data:
        if comet == item['object']:
            comet_desired = item
            for data in comet_data:
                comet_dict[data] = comet_desired[data]
            comet_list.append(comet_dict)
    return json.dumps(comet_list, indent=2)





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
