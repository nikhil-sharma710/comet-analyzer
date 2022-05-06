from flask import Flask, jsonify, request
import logging
import json

logging.basicConfig(level=logging.DEBUG)

# redis_ip = os.environ.get('REDIS_IP')
app = Flask(__name__)
# rd = redis.Redis(host=redis_ip, port=6379, db=0)

# comets_data = {}


@app.route('/read_data', methods=['POST'])
def read_data_from_file():
    """
    
    """

    logging.info('Reading data...')

    global comets_data

    with open('comets_data.json', 'r') as f:
        comets_data = json.load(f)

    return f'Data has been read from file\n'


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
    for item in comets_data:
        comets_names.append(item['object'])

    return json.dumps(comets_names, indent=2)


@app.route('/comets/<comet>', methods=['GET'])
def get_comet_info(comet):
    """

    """

    logging.info('Querying route to get all info on /' + comet)

    comet_dict = {}
    comet_list = []
    comet_data = ['epoch_tdb', 'tp_tdb', 'e', 'i_deg', 'w_deg', 'node_deg', 'q_au_1', 'q_au_2', 'p_yr', 'moid_au', 'ref', 'object_name']

    for item in comets_data:
        specific_comet = item['object']
        if comet == specific_comet:
            comet_desired = item
            for data in comet_data:
                comet_dict[data] = comet_desired[data]
            comet_list.append(comet_dict)
    return json.dumps(comet_list, indent=2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
