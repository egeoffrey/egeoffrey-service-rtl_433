### service/rtl_433: interact with an attached RTL-SDR device
## HOW IT WORKS: 
## DEPENDENCIES:
# OS: rtl_433
# Python: 
## CONFIGURATION:
# required: command
# optional: 
## COMMUNICATION:
# INBOUND: 
# OUTBOUND:
# - controller/hub IN: 
#   required: 
#   optional: filter, measure

import datetime
import json
import time
import json
import subprocess
import shlex

from sdk.python.module.service import Service
from sdk.python.utils.datetimeutils import DateTimeUtils
from sdk.python.module.helpers.message import Message

import sdk.python.utils.datetimeutils
import sdk.python.utils.command
import sdk.python.utils.exceptions as exception

class Rtl_433(Service):
    # What to do when initializing
    def on_init(self):
        # map sensor_id with service's configuration
        self.sensors = {}
        # require configuration before starting up
        self.config = {}
        self.config_schema = 2
        self.add_configuration_listener("house", 1, True)
        self.add_configuration_listener(self.fullname, "+", True)
        
    # What to do when running
    def on_start(self):
        # request all sensors' configuration so to filter sensors of interest
        self.add_configuration_listener("sensors/#", 1)
        # kill rtl_433 if running
        sdk.python.utils.command.run("killall rtl_433")
        # run rtl_433 and handle the output
        command = self.config['command']+" "+self.config['arguments']
        self.log_debug("running command "+command)
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        prev_output = ""
        while True:
            # read a line from the output
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                # process ended, break
                self.log_info("rtl_433 has ended")
                break
            if output:
                # output available
                try:
                    # avoid handling the same exact output, skipping
                    if prev_output == output: continue
                    # parse the json output
                    json_output = json.loads(output)
                except Exception,e:
                    # not json format, ignoring
                    continue
                self.log_debug("Received: "+str(json_output))
                # for each registered sensor
                for sensor_id in self.sensors:
                    sensor = self.sensors[sensor_id]
                    # apply the filter if any
                    if "filter" in sensor:
                        search = {}
                        if "&" in sensor["filter"]: key_values = sensor["filter"].split("&")
                        else: key_values = [sensor["filter"]]
                        for key_value in key_values:
                            if "=" not in key_value: continue
                            key, value = key_value.split("=")
                            search[key] = value
                        # check if the output matches the search string
                        found = True
                        for key, value in search.iteritems():
                            # check every key/value pair
                            if key not in json_output: found = False
                            if str(value) != str(json_output[key]): found = False
                        if not found: continue
                    # prepare the message
                    message = Message(self)
                    message.recipient = "controller/hub"
                    message.command = "IN"
                    message.args = sensor_id
                    value = json_output[sensor["measure"]] if "measure" in sensor and sensor["measure"] in json_output else 1
                    message.set("value", value)
                    # send the measure to the controller
                    self.send(message)
                    self.log_debug("Matched sensor "+sensor_id+" with value "+str(value))
                # keep track of the last line of output
                prev_output = output

    
    # What to do when shutting down
    def on_stop(self):
        pass

    # What to do when receiving a request for this module
    def on_message(self, message):
        pass

    # What to do when receiving a new/updated configuration for this module    
    def on_configuration(self,message):
        # module's configuration
        if message.args == self.fullname and not message.is_null:
            # upgrade the config schema
            if message.config_schema == 1:
                config = message.get_data()
                config["arguments"] = "-F json -U"
                self.upgrade_config(message.args, message.config_schema, 2, config)
                return False
            if message.config_schema != self.config_schema: 
                return False
            # ensure the configuration file contains all required settings
            if not self.is_valid_configuration(["command", "arguments"], message.get_data()): return False
            self.config = message.get_data()
        # register/unregister the sensor
        if message.args.startswith("sensors/"):
            if message.is_null: 
                sensor_id = self.unregister_sensor(message)
            else: 
                sensor_id = self.register_sensor(message, ["filter"])
