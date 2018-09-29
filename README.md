## What is micro-Waggle?

## Why micro-Waggle? 

## Getting Started 

### 1. Devices and Accounts: 

The micro-Waggle is a project designed to work on the [Particle.io](https://www.particle.io/what-is-particle) platform. Micro-Waggles can be programmed through one of the following Particle.io devices:
- [Particle Photon](https://store.particle.io/collections/photon#photon)   : Wifi based device 
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/photon.png" width="300">

- [Particle Electron](https://store.particle.io/collections/electron#electron) : Cellular based device
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/electron_1.png" width="300">

In order to proceed, you can create a Particle.io account [here](https://login.particle.io/signup).

### 2. Register your Device and get your Particle Access Token: 

After your Particle.io account is set up, your devices can be registered to your account via this [link](https://setup.particle.io/). The devices registered on your account can be veiwed through the Particle.io [Console](https://console.particle.io/devices). At this point you can recognize the device IDs for your devices set by Particle.io. The particle.io console should look like this: 
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/devices.png" width="600">

You can simply click on the device ID you seek to visit the page specific to the selected device (The link should look like this: https://console.particle.io/devices/YOUR_DEVICE_ID). Particle.io also provides an Integrated Web based Development Environment(IDE). The platform also provides detailed [documentation](https://docs.particle.io/guide/getting-started/build/photon/#web-ide) on working your way around the Web IDE. Moving forward, it is necessary to seek out the [Access Token](https://docs.particle.io/guide/how-to-build-a-product/authentication/#what-39-s-an-access-token-) tied to your Particle.io account. Reading data as well as sending commands to your devices can only be done through an Access Token. Access Token can be easilly gained thorugh the Particle.io [Build](https://build.particle.io/build/) page.

Once on the said page, click on the settings icon on the lower left hand corner of the page. The settings icon is emphazied below:

<img src="https://github.com/waggle-sensor/microWaggle/blob/master/integrated/resources/settings.png" width="300">


This will result in your Access token being displyed on the left hand side of the page as demostrated here:
<img src="https://github.com/waggle-sensor/microWaggle/blob/master/integrated/resources/accessToken.png" width="300">


### 3. Start with a Blink:
Once you are familiar with the Particle.io Web IDE, you can go ahead and program your first application for your device. Particle.io provides a basic implimentation of an LED Blink [programme](https://docs.particle.io/guide/getting-started/build/photon/#flashing-your-first-app) to get you started. Once impliemented you will see your Photon/Electron flashing its LED on pin D7. 

### 4. Building and programming generic micro-Waggle code:
Micro-Waggle devices works under a unique design in which they read and publish data. The code found [here](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/firmware/microWaggle.ino) gives a generic implimentation of a micro-Waggle application. In the same manner you flashed the [Blink app](https://docs.particle.io/guide/getting-started/build/photon/#flashing-your-first-app) on to your device, you can flash the generic micro-Waggle code onto your device. 

### 5. See streaming data from the sensors: 
After flashing the generic [code](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/firmware/microWaggle.ino), you can check the data being published on the Particle.io cloud through the Particle.io [Console](https://console.particle.io/events).  At this time the Particle.io Console would look like this:
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/resources/events.png">

### 6. Control the device from your computer: 
The micro-Waggle platform allows its users to control there devices remotely via the Particle.io cloud. The [deviceController](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/software/deviceController/) module enables this facilty.

#### 6.1 Using the test node at Argonne National Labs(ANL) 
This module can readilly be used through the Particle.io device already set up for testing at ANL. The node runs the generic micro-Waggle program described above. You can start by following the instructions given [here](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/software/deviceController/readme.md). Make sure to include the details given below when setting up your local Node Configuration:
- Device ID    : 53002a000c51353432383931
- Access Token : c9003c4f929c03b67daac131a84b9d3aa3d75e3e
- Use the default micro-Waggle Config: True

You are free to use any appropriate inputs for the rest of the prompts. After setting up your local configuration file you will have control over the test node set up. Make sure to try out different configurations before moving forward. To seek how the 
Node responds you may visit this [link](https://api.particle.io/v1/devices/events?access_token=c9003c4f929c03b67daac131a84b9d3aa3d75e3e) which publishes the data coming out of the said Node. 

#### 6.2 Using your own node 
This can be done through following similar steps descibed above. Make sure to replace the device ID and the Access Token with the desired credentials belonging to your Particle.io device. The data streams which is published through your device can be seen through the Particle.io [Console](https://console.particle.io/events).  

### 7. Get Beehive publish credentials:
The micro-Waggle project keeps all its data at ANLs Beehive Server. Beehives publish credentials can be requested through the Waggle team at ANL.

### 8. Run relayServer to send data to Beehive: 
Particle.io devices can only publish its data to the Particle.io cloud. As such, a separate tool is used to send data from the cloud to the Beehive server. The [relayServer](https://github.com/waggle-sensor/microWaggle/tree/master/integrated/software/relayServer) module is designed to manage this task. 
 
#### 8.1 Using the test node at ANL
Again for the use of the relayServer module you may use the test Node set up at ANL. As descibed [here](https://github.com/waggle-sensor/microWaggle/tree/master/integrated/software/relayServer/readme.md), make sure to obtain the necessary credentials for the Relay server module to connect to Beehive. 
Since the device ID for the Particle.io device at Argonne is '53002a000c51353432383931' the directory structure for the use of the test node shoud look like this:
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
After the initial implimentation of the `relay-server.py` with no args. -> `python3 relay-server.py` make sure to include the access token 'c9003c4f929c03b67daac131a84b9d3aa3d75e3e' within the `nodeConfig.json`.
The later instructions given on the releyServer module would be sufficient in moving forward. 

#### 8.2 Using your own node
The instructions given [here](https://github.com/waggle-sensor/microWaggle/blob/master/integrated/software/relayServer/readme.md) on the releyServer module would be sufficient in setting up your own Node. 

### 9. Check data from device: 
Once the relayServer is online, in less than 5 minutes you should see micro-Waggle data being published on [Beehive](https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php). The data will come under the link label: MWTesting.complete.recent.csv.

### 10. Tweak the micro-Waggle behavior and see changes on Beehive: 

At this point you are in a position to modify the generic micro-Waggle [code](https://github.com/waggle-sensor/summer2018/blob/master/microWaggle/integrated/firmware/microWaggle.ino) and flash it into your Particle.io devices. After such changes are made, you can observe its effects through [Beehive](https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php). 

### 11. Code your own micro-Waggle device:

Congratulations, you are ready to impliment your own microWaggle implimentation. Particle.io's example [log](https://docs.particle.io/guide/getting-started/examples/photon/) is good place to get you started. Make sure to contact the Waggle team at ANL for further support.

------------------------------------------------------------

#### Helpful resources:
- [Photon Documentation](https://docs.particle.io/guide/getting-started/examples/photon/).
- [Electron Documentation](https://docs.particle.io/guide/getting-started/examples/electron/).




