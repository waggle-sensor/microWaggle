## What is micro-Waggle?
The micro-Waggle is an implementation of the Waggle platform for Particle.io devices. It communicates with the Waggle Beehive via small packets of data called sensorgrams. Data from micro-Waggle devices appears alongside data from other Waggle implementations such as Chicago's AoT network and can be retreived by identical methods.

## Why micro-Waggle? 
Micro-Waggle provides a means to deploy lightweight, low-footprint sensor packages as part of a network of Waggle nodes in order to capture varied kinds of data in diverse environments.

## Getting started 

### 1. Devices and accounts
The micro-Waggle has been implemented on two Particle products:
- [Particle Photon](https://store.particle.io/collections/photon#photon)   : Wifi based device 
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/photon.png" width="300">

- [Particle Electron](https://store.particle.io/collections/electron#electron) : Cellular based device
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/electron_1.png" width="300">

These devices communicate with the Particle Cloud and must be claimed and set up in order to retreive data. You can create a Particle.io account [here](https://login.particle.io/signup). **You need an account to view the Particle Console and Build environments.** You can only view data from a device you have registered to your account.

Once you have set up your account, [set up](https://setup.particle.io/) your Particle on your Wifi network, claim your first device, and register it to your account.

### 2. Getting familiar with the platform
The devices registered on your account can be veiwed through the Particle.io [Console](https://console.particle.io/devices). At this point you can recognize the device IDs for your devices set by Particle.io. The particle.io console should look like this: 
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/devices.png" width="600">

You can simply click on the device ID you seek to visit the page specific to the selected device (The link should look like this: https://console.particle.io/devices/YOUR_DEVICE_ID). Particle.io also provides a Web based Integrated Development Environment (IDE) and detailed [documentation](https://docs.particle.io/guide/getting-started/build/photon/#web-ide) for its use.

Similar to Arduino, each piece of Particle firmware requires a "Setup" portion which runs on each startup of the device and a "Loop" portion which repeats and which governs the normal operation of the device. If this is your first time working with a Particle.io device or you are unfamiliar with Arduino-like platforms, it is recommended that you try out the demonstration programs, including the classic "Blink", on the Particle Build page. Particle has provided detailed [documentation](https://docs.particle.io/reference/device-os/firmware/photon/) on the features and capabilities of your device.

At this point, try to flash some working code (such as Blink) to the device. You may want to use the Particle [command-line interface (CLI)](https://docs.particle.io/reference/developer-tools/cli/) to do this, or you can do it via the web IDE. Once you are comfortable with the device, you can start setting up your micro-Waggle.

### 3. Building and programming generic micro-Waggle code
Micro-Waggle devices convert data into a machine-readable string that the Waggle Beehive server can interpret. The code found [here](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/firmware/microWaggle.ino) gives a generic implementation of a micro-Waggle application for the Particle Photon. This code can be copied and pasted into the Particle Build IDE and flashed to your device "over the air". Alternatively, you can compile it and flash it to the Photon via serial using the Particle CLI.

The default setup for the micro-Waggle publishes dummy data (the integer "5") as the output of each sensor, and includes two dummy sensors ("temp" and "humidity") for you to test changing measurement frequencies with. To add your own sensors, you must add code to the the micro-Waggle firmware which reads a sensor as part of the loop.

### 4. See streaming data from the sensors
After flashing the generic [code](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/firmware/microWaggle.ino), you can check the data being published on the Particle.io cloud through the Particle.io [Console](https://console.particle.io/events).  On an individual device's page, you can see details about that device's data stream. On the Particle Console's [Events](https://console.particle.io/events) page, you can view the data stream from all of your devices.
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/events.png">

### 5. Get your Access Token
To access data from your Particle device and to send it commands without visiting the Particle Console, you will need your permanent [Access Token](https://docs.particle.io/guide/how-to-build-a-product/authentication/#what-39-s-an-access-token-) which is tied to your Particle.io account. Visit the Particle.io [Build](https://build.particle.io/build/) page and click on the settings icon on the lower left hand corner of the page (below) to find your token.

<img src="https://github.com/waggle-sensor/microWaggle/blob/master/integrated/resources/settings.png" width="300">       <img src="https://github.com/waggle-sensor/microWaggle/blob/master/integrated/resources/accessToken.png" width="300">

### 6. Control the device from your computer
The micro-Waggle generic firmware allows a user to control devices remotely via the Particle Cloud. You can configure your device via the Particle.io Console by sending arguments to the sensorConfig and nodeConfig functons as descibed [here](https://github.com/waggle-sensor/microWaggle/tree/master/integrated/software/deviceController#micro-waggle-devicecontroller-through-the-particleio-console). The [deviceController](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/software/deviceController/) module provides this functionality from a terminal. The deviceController requires Python 3 with json, requests, os, sys, and pprint packages.

### 7. Get Beehive publish credentials:
The micro-Waggle project keeps all its data at ANL's Beehive Server. Beehive publish credentials can be requested from the Waggle team at ANL.

### 8. Run relayServer to send data to Beehive: 
Particle.io devices can only publish its data to the Particle.io cloud. As such, a separate tool is used to send data from the cloud to the Beehive server. The [relayServer](https://github.com/waggle-sensor/microWaggle/tree/master/integrated/software/relayServer) module is designed to manage this task. 
 
As descibed [here](https://github.com/waggle-sensor/microWaggle/tree/master/integrated/software/relayServer/readme.md), make sure to obtain the necessary credentials for the Relay server module to connect to Beehive. 
Since the device ID for our test device at Argonne is '53002a000c51353432383931' the directory structure for the use of the test node shoud look like this:
```bash
├── parentDirectory
│   ├── relay-server.py
│   ├── devices
│   │   ├──53002a000c51353432383931
│   │   │   ├──node_id
│   │   │   ├──cacert.pem
│   │   │   ├──key.pem 
│   │   │   ├──cert.pem
```
Your directory structure will be identical, with a separate folder for each device.

After the initial implimentation of the `relay-server.py` with no args. -> `python3 relay-server.py` make sure to include your access token within the `nodeConfig.json`.
To move forward with setting up the relay server, read the documentation for that module.


### 9. Check data from device
Once the relayServer is online, in less than 5 minutes you should see micro-Waggle data being published on [Beehive](https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php). The data will come under the link label: MWTesting.complete.recent.csv.

### 10. Tweak the micro-Waggle behavior and see changes on Beehive
At this point you are in a position to modify the generic micro-Waggle [code](https://github.com/waggle-sensor/summer2018/blob/master/microWaggle/integrated/firmware/microWaggle.ino) and flash it into your Particle.io devices. After such changes are made, you can observe its effects through [Beehive](https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php). 

### 11. Code your own micro-Waggle device
Congratulations, you are ready to impliment your own micro-Waggle implimentation. Try adding real sensors and changing their behavior. Make sure to contact the Waggle team at ANL for further support.

------------------------------------------------------------

#### Helpful resources:
- [Photon Documentation](https://docs.particle.io/guide/getting-started/examples/photon/).
- [Electron Documentation](https://docs.particle.io/guide/getting-started/examples/electron/).




