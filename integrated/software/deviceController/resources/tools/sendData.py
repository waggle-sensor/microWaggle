#----This sends function cmds to the photon---
#In terminal, run "python sendData.py [functionName] "[parameter]"
  # ** make sure to put quotation marks around the parameter that you send

import json
import requests
import time
import sys

# args[0] = function name
# args[1] = parameter to send

args = sys.argv[1:]
access_token = ""
deviceId = ""
function = args[0]

print(args[0] + "(" + args[1] + ")")

payload = {'params': args[1], 'access_token':access_token}
requests.post("https://api.particle.io/v1/devices/{0}/{1}/"
                          .format(deviceId, function), payload)


# https://api.particle.io/v1/devices/events?access_token=
