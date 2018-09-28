# User Control
_*** **NOTE** ***:  `usercontrol.io` is NOT the completed, final file. This is just the code that pertains to enabling usercontrol on the photon. Individual, specific projects of the MicroWaggle Project will have to integrate this code in their final program, given that they edit this file to their needs._
- `usercontrol.ino` allows changing configurations of the node sensors and the node itself from the particle console (and from a python script, like `sendData.py`)
- The Particle Photon holds a list of sensors that it currently has, and frequently sends status messages to the Particle Cloud indicating the status of each sensor (i.e., the sensor's sensing frequency and current status of either Enabled or Disabled)

## Controlling the Particle Photon from Particle Console
- Once your Photon is setup, connected to internet, and running usercontrol.ino, go to [Particle Console](https://console.particle.io/)
- Once you're in the Particle Console, go to your device (should be a link like https://console.particle.io/devices/YOUR_DEVICE_ID), you will see events being published and you can also see the 2 particle functions - `sensorConfig()` and `nodeConfig()`
- From here you will recieve 3 types of events: 
    * microWaggleStatus
    * sensorgram
    * ERROR
- Below is a diagram depicting the different events being sent from Photon to Particle Cloud ![alt text](https://github.com/waggle-sensor/summer2018/blob/master/bike_waggle/controller/User%20Control%20Diagram.png "User Control Events")
### microWaggleStatus
* Sends a frequent update showing the status of each sensor, the SD card, and the reporting frequency of the node. 
* Format: `"sensorId:sensorName,sensorStatus,sensingFrequency;SD:sdStatus;ReportFreq:nodeReportingFrequency"`
    * the `sensorId:sensorName,sensorStatus,sensingFrequency` is repeated for every sensor, so if there are 5 sensors, that block will be repeated 5 times for each sensor
    * **status** - the `status`, like `sensorStatus` or `sdStatus`, represents if it is **enabled** or **disabled**. The status will either say 
        * `en` for **Enabled**, or 
        * `dis` for **Disabled**
    * **frequencies** - is in seconds
    * Example microWaggleStatus output: **`1:tempSensor,en,15;2:humiditySensor,dis,30;SD:en;ReportFreq:60`**
### Sensorgram
* The sensorgram that is being sent is just dummy data. Actual, current, up-to-date sensorgram formats and sending protocal is under `/bike_waggle/sensorgram` folder in summer2018 repository
* `pack(sensorID, sensor_instance, parameter_id, data, time)` - the pack function takes in data to construct a sensorgram. It returns a sensorgram as a Hex String representation.
* `IntToHex()`, `ShortToHex()`, `CharToHex()` - used in pack function. 
    * *****For all future code that is being written, remove these functions and use Particle's built-in function to convert a datatype into a Hex String. Use `Particle.String(someDataHere, HEX);` → See [Docs](https://docs.particle.io/reference/firmware/photon/#string-) for more details
* The pack function to build a sensorgram is called every X number of seconds (i.e., the number of seconds is the sensing frequency of each sensor)
* Once a sensorgram is constructed, it is appended onto a larger string that holds all the sensorgrams. If the length of the large string exceeds `maxPublishingLength`, then a semi-colon is appended onto the string.
* Once the time has exceeded the `reporting frequency`, `PublishData()` is called. This sends either all the data in the large string if there is no semicolon, or if there is a semicolon, it sends only the data uptill the first semi colon
    * This is to ensure that too much data isn't being sent in one publish, as the Particle Photon can only send a max of _about_ 622 bytes (or characters).***
* Below is a diagram depicting the sensorgram process of constructing and uploading to the cloud. **Note: Instead of sending data straight to Particle Cloud, it can send it to an SD card if there is no Internet Connection, and then send the data from the SD card to Particle Cloud once internet connection is restored
![alt text](https://github.com/waggle-sensor/summer2018/blob/master/bike_waggle/controller/Sensorgram%20Process.png "Sensorgram Process")

### Error Messages
- Error messages are sent with the the Particle Event name "ERROR"
- An error messages is sent if an invalid input is sent to `sensorConfig()` or `nodeConfig()`

## Controlling the Particle Photon from CLI
- It is also possible to send user control commands to the Particle Photon from the CLI through the `controller.py`. Please refer to the documentation for `controller.py` for more details on how to send commands to Particle Photon from the command line interface

## Default Parameters
- **Following are the default values for various configurations. These can be changed per project's needs
- SD Card - Disabled
- Reporting Frequency (how often the Photon publishes sensorgram data) - 60 seconds
- Frequency of Status Messages (how often status msgs are sent) - 10 seconds
- Max Publishing Length (max number of characters that can be sent in one Particle Publish to cloud ) - 600 bytes (or characters)
    * the max amount Particle Publish can send is 622 bytes, so do not exceed that limit of 622 bytes!

## User-Control Functions
### nodeConfig
- allows users to manage their preferences for the node, the Particle Photon, as a whole
- The user must submit a parameter from their end, which is then received by the nodeConfig function and processed appropriately
- Can be used for:
   * enabling/disabling the reporting of sensor data for all sensors of the node
   * enabling/disabling the usage of an SD card when reporting sensor data
   * changing the frequency of reporting sensor data
- Parameters:
   * “enableAll” – enables reporting of sensor data for all sensors of node
   * “disableAll” – disables reporting of sensor data for all sensors of node
   * “enableSD” – enables reporting of sensor data to the SD card
   * “disableSD” – disables reporting of sensor data to the SD card
   * “freqReport-[secs]” – changes frequency of reporting sensor data to [secs] seconds
### sensorConfig
- allows users to manage their preferences for individual sensors of a specific node/Photon
- The user must submit a parameter from their end, which is then received by the sensorConfig function and processed appropriately. 
- Can be used for:
   * enabling/disabling the reporting of sensor data for a specific sensor
   * changing the frequency of reporting sensor data for a specific sensor.
- Format of the parameter to send: “sensorID;status;frequency”
- Parameters:
   * sensorID:
      * the ID of the sensor you are trying to change preferences for
   * status:
      * “en” – enables reporting of sensor data for specified sensor
      * “dis” – disables reporting of sensor data for specified sensor
      * “_” – use as a placeholder for when no changes to the status of the sensor are wanted
   * frequency:
      * [secs] – changes frequency of reporting sensor data for the specified sensor to [secs] seconds
      * “_” – use as a placeholder for when no changes to the frequency of the sensor are wanted



      
