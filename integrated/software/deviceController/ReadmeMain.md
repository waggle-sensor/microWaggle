# DeviceController

The device controller module gives users of microWaggle nodes a form of remote user control. The module is capable of changing frequencies of reading and publishing data as well as enabling & disabling of device sensors. 
 
## Micro-Waggle deviceController CLI guide

The device controller module lets you manage a microWaggle node network through a CLI. It should be noted that the **access tokens** and the unique **device IDs** privided by Particle.io needs to be at hand before the implimentation of the module. 

## First time usage: 
- Run `controller.py` with no args. -> `python3 controller.py`. The`--help` prompt gives you the basic options that the controller provides.
- On its initial run`controller.py` will create `nodeConfig.json` file which will keep the node configuration the user intends to keep. Everytime the module is implimented, it will seek to mimic the configuration defined on `nodeConfig.json`on the actual microWaggle network.  
- 

## Usage

### 


* **The script must be run in PYTHON3 with one of the following args seen below:**

`--help` or `help` : Lists all commands, as well as their respective syntaxes and functions.

* Ex. Usage: `python3 controller.py --help` 

`--list [OPTIONAL ARGS: -sen <nodeID>]`: Lists all nodes, respective information such as nodeID and deviceID, and sensor configuration. Using the `-sen` flag will list all sensors and their attributes on the given `nodeID`.
* Ex. Usage: `python3 controller.py --list`
* Ex. Usage, **Given that node with ID 22 exists**: `python3 controller.py --list -sen 22`

`--enAll` : Enables all sensors on on all nodes.
* Ex. Usage: `python3 controller.py --enAll`

`--disAll` : Disables all sensors on all nodes.
* Ex. Usage: `python3 controller.py --disAll`

`--rm <nodeID>` : removes the node with the specified name
* Ex. Usage, **Given a node with nodeID 33 exists** : `python3 controller.py --rm <nodeID>`

`--add` : Starts the prompt to add a new node.
* Ex. Usage: `python3 controller.py --add`

`--configure <nodeID> [-rn/-id/-d/-e/-sdf/-ssf/-sm/-sd/-sen]`
* Ex. Usage: **See below**

## The configure command

The configure command is the main attraction, and how you modify your node. Here are the args you can use.

`-rn <new name>` : Renames the entered node. You can specify multiply nodes to rename to the same thing, by putting a comma in between the nodes you want to rename. Ex. Usage below. 
* **NODE NAMES CANNOT HAVE SPACES!**
* Ex. Usage, **Given a node with the nodeID 33 exists**: `python3 controller.py --configure 33 -rn bar` -> Node 33 is now named bar.
* Ex. Usage, **Given nodes with the nodeID 33, 99, and 66 exist**: `python3 controller.py --configure 33,66,99 -rn Field_node` -> nodes with the nodeID 33, 66, and 99 are now named "Field_node".


`-id <new nodeID>` : changes the nodeID of the entered node. 
* Ex. Usage, **Given a node with the nodeID 33 exists**: `python3 controller.py --configure 33 -id 96024` -> Node with ID 33 now has the nodeID 96024.
* Node ID's certaintly don't have to have numbers or letters exclusively, as the controller supports both. However, try to keep it concise. I haven't tested the controller with longer, more complex ID's, so they may not work. Please contact me if you have any issues regarding this.
* **USE CAREFULLY. ANY CHANGES DONE TO A NODE WITH A SPECIFIED ID WILL BE DONE TO ALL NODES WITH THE MATCHING ID.**

`-d` : Disables all sensors on the given node. Can disable all sensors on more than one node at once if the nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 34 exists**: `python3 controller.py --configure 34 -d` -> Node with ID 34 is disabled.
* Ex. Usage, **Given nodes with the nodeID 35, 36, 37, & 38 exist**: `python3 controller.py --configure 35,36,37,38 -d` -> Sensors on nodes with ID 35, 36, 37, & 38 are disabled.

`-e` : Enables all sensors on the given node. Can enable all sensors on more than one node at once if the nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 34 exists**: `python3 controller.py --configure 34 -e` -> Node with ID 34 is enabled.
* Ex. Usage, **Given nodes with the nodeID 39, 40, 41, & 42 exist**: `python3 controller.py --configure 39,40,41,42 -e` -> Sensors on nodes with ID 39, 40, 41, & 42 are enabled.

`-sdf <new sending frequency in seconds>` : Changes the frequency at which the selected node sends data. Can change multiple node's setting if nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 43 exists**: `python3 controller.py --configure 43 -sdf 15` -> Node with ID 43 now has a sending frequency of 15 seconds. 
* Ex. Usage, **Given nodes with the nodeID 44, 45, and 46 exist**: `python3 controller.py --configure 44,45,46 -sdf 15` -> Nodes ID 44, 45, & 46 now have a sending frequency of 15 seconds. 

`-ssf <new sensing frequency in seconds>` : Changes the frequency at which the selected node senses data. Can change multiple node's setting if nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 47 exists**: `python3 controller.py --configure 47 -ssf 15` -> Node with ID 47 now has a sensing frequency of 15 seconds. 
* Ex. Usage, **Given nodes with the nodeID 48, 49, and 50 exist**: `python3 controller.py --configure 44,45,46 -ssf 15` -> Nodes ID 48, 49, & 50 now have a sensing frequency of 15 seconds.

`-sm <True/False>` : Sets if the node should send a status message periodically. True = Yes, False = No. You can use this command on multiple nodes, provided there's a comma in between the nodeIDs. Example usage below. 
* Ex. Usage: `python3 controller.py --configure 51 -sm True` -> Node with the ID 51 will send status messages.
* Ex. Usage: `python3 controller.py --configure 52,53,54,55,56 -sm False` -> Node with the IDs 52, 53, 54, 55, & 56 will not send status messages.

`-sd <True/False>` : Sets if the node should save data to SD storage when disconnected from Wi-Fi. True = Yes, False = No. You can use this command on multiple nodes, provided there's a comma in between the nodeIDs. Example usage below. 
* Ex. Usage: `python3 controller.py --configure 57 -sd True` -> Node with the ID 51 will store to SD.
* Ex. Usage: `python3 controller.py --configure 58,59,60,61,62 -sm False` -> Node with the IDs 58, 59, 60, 61, & 62 will not save to SD storage.

### The sen configure commmand

The `-sen` subcommand of the `--configure` command has two parts, so it gets it's own subsection. This is where you can configure individual sensors on your node without having to make a new Node/Configuration.

`-sen add` : Adds a new sensor to the the given node. It will take you through the prompt for adding a new sensor. If you specify multiple nodes in this command, the sensor form you fill out will be applied to **all** nodes specified. 

* Ex. Usage: `python3 controller.py --configure 63 -sen add
* Ex. Usage: `python3 controller.py --configure 64,65,66,67 -sen add

`-sen rm <sensor ID to remove>` : Removes a sensor from the given node. If you specifiy multiple nodes in this command, the sensor will be removed on each node, **provided the sensor with the corresponding ID exists**. If it doesn't exist, no worries! Nothing bad will happen.
* Ex. Usage: `python3 controller.py --configure 68 -sen rm 01` -> Sensor 01 gets removed from node with ID 68.
* Ex. Usage: `python3 controller.py --configure 69, 70 -sen rm 01` -> Sensor 01 gets removed from nodes with ID's 69 & 70.

`-sen dis <sensor ID to disable>` : Disables the selected sensor. If you specify multiple sensors using this command, all sensors specified will be affected. 
* **THIS DOES NOT WORK FOR MULTIPLE NODES AS OF VERISON 1, AND WILL BE ADDED LATER.** 
* Ex. Usage, **Given node 71 with sensor with ID 0 exists**: `python3 controller.py --configure 71 -sen dis 0`


`-sen en <sensor ID to disable>` : Enables the selected sensor. If you specify multiple sensors using this command, all sensors specified will be affected. 
* **THIS DOES NOT WORK FOR MULTIPLE NODES AS OF VERISON 1, AND WILL BE ADDED LATER.** 
* Ex. Usage, **Given node 72 with sensor with ID 0 exists**: `python3 controller.py --configure 72 -sen en 0`

`-sen freq [sensing frequency in seconds] <sensor ID to affect>` : Changes the frequency of sensing for the selected sensor.
* Ex. Usage, **Given node 73 with sensor with ID 0 exists**: `python3 controller.py --configure 73 -sen freq 45 0`

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



      
