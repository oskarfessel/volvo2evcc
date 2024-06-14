import logging
import time
import json
import volvo
import util
import os
from threading import Thread, Timer
from datetime import datetime
from babel.dates import format_datetime
from config import settings
from const import CLIMATE_START_URL, CLIMATE_STOP_URL, CAR_LOCK_URL, \
    CAR_UNLOCK_URL, availability_topic, icon_states, old_entity_ids, otp_mqtt_topic


values = {}
assumed_climate_state = {}
last_data_update = None
climate_timer = {}
engine_status = {}
devices = {}
active_schedules = {}
otp_code = None

def update_loop():
    while True:
        if settings["updateInterval"] > 0:
            logging.info("Fetching volvo vehicle data...")
            update_car_data()
            logging.info("Fetching data done. Next run in " + str(settings["updateInterval"]) + " seconds.")
            time.sleep(settings["updateInterval"])
        else:
            logging.info("Data update is disabled, doing nothing for 30 seconds")
            time.sleep(30)


def update_car_data(force_update=False, overwrite={}):
    global last_data_update
    global values
    last_data_update = format_datetime(datetime.now(util.TZ), format="medium", locale=settings["babelLocale"])
    for vin in volvo.vins:
        result = {}
        for entity in volvo.supported_endpoints[vin]:
            logging.debug("Entity: " + str(entity))
            if entity["domain"] in ["button"]:
                continue

            ov_entity_id = ""
            ov_vin = ""
            ov_state = ""
            if bool(overwrite):
                ov_entity_id = overwrite["entity_id"]
                ov_vin = overwrite["vin"]
                ov_state = overwrite["state"]

            if entity["id"] == "climate_status":
                state = assumed_climate_state[vin]
            elif entity["id"] == "last_data_update":
                state = last_data_update
            elif entity["id"] == "active_schedules":
                logging.debug("ACTIVE SCHEDULES FOUND") 
                #state = active_schedules[vin]
            elif entity["id"] == "update_interval":
                state = settings["updateInterval"]
            elif entity["id"] == "api_backend_status":
                if force_update:
                    state = volvo.get_backend_status()
                else:
                    state = volvo.backend_status
            else:
                if entity["id"] == ov_entity_id and vin == ov_vin:
                    state = ov_state
                else:
                    state = volvo.api_call(entity["url"], "GET", vin, entity["id"], force_update)
            result[entity["id"]] = state
            logging.debug("state = " + str(state))
        values[vin] = result
        logging.debug("values = " + str(values))
        """
            if entity["domain"] == "device_tracker" or entity["id"] == "active_schedules":
                topic = f"homeassistant/{entity['domain']}/{vin}_{entity['id']}/attributes"
            elif entity["id"] == "warnings":
                mqtt_client.publish(
                    f"homeassistant/{entity['domain']}/{vin}_{entity['id']}/attributes",
                    json.dumps(state)
                )
                if state:
                    state = sum(value == "FAILURE" for value in state.values())
                else:
                    state = 0

                topic = f"homeassistant/{entity['domain']}/{vin}_{entity['id']}/state"
            else:
                topic = f"homeassistant/{entity['domain']}/{vin}_{entity['id']}/state"

            if state or state == 0:
                mqtt_client.publish(
                    topic,
                    json.dumps(state) if isinstance(state, dict) or isinstance(state, list) else state
                )
                update_ha_device(entity, vin, state)
        """

