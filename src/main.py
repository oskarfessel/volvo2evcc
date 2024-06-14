import logging
import volvo
import threading
import evcc
from const import VERSION
from util import set_tz, setup_logging, set_mqtt_settings, validate_settings
from flask import Flask, jsonify

host_name = "192.168.0.1"
port = 8182
values = {}

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    logging.info("REST service called. Values are: " + str(evcc.values))
    return jsonify({'data': evcc.values})


if __name__ == '__main__':
    setup_logging()
    logging.info("Starting volvo2evcc version " + VERSION)
    validate_settings()
    set_tz()
    volvo.authorize()
    logging.info("Volvo vins: " + str(volvo.vins))
    logging.info("values: " + str(values))
    for vin in volvo.vins:
        device = volvo.get_vehicle_details(vin)
    #app.run(host=host_name, port=port, debug=True, use_reloader=False)
    threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()
    evcc.update_loop()
