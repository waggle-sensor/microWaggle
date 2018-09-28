## What is micro-Waggle?

## Why micro-Waggle? 

## Getting Started 

### 1. Devices and Accounts: 

The micro-Waggle is designed to work on [Particle.io](https://www.particle.io/what-is-particle) platform. Micro-Waggle devices can be programmed through one of the following Particle.io devices:
- [Particle Photon](https://store.particle.io/collections/photon#photon)   : Wifi based device  
- [Particle Electron](https://store.particle.io/collections/electron#electron) : Cellular based device

In order to proceed, you can create a Particle.io account [here](https://login.particle.io/signup).

### 2. Register your Device and get your Particle Access Token: 

After your Particle account is set up, your particle devices can be registered to your account via this [link](https://setup.particle.io/). The devices registered on your account can be veiwed through the Particle.io [Console](https://console.particle.io/devices). At this point you can recognize the Device IDs for your devices set by Particle.io. The page should look like this: 
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/microWaggle/Resources/Particle_Devices.png?token=AYVA9OxrQZVuTp78bo5Ww7WGsjA30t9Xks5bs-VIwA%3D%3D">

You can simply click on the device ID you seek to visit the page specific to the selected device (The link should look like this: https://console.particle.io/devices/YOUR_DEVICE_ID). Particle.io also provides an Integrated Web based Development Environment(IDE). The platform also provides detailed [documentation](https://docs.particle.io/guide/getting-started/build/photon/#web-ide) on working your way around the Web IDE. Moving forward, it is necessary to seek out the [access token](https://docs.particle.io/guide/how-to-build-a-product/authentication/#what-39-s-an-access-token-) tied to your Particle.io account. Reading data as well as sending commands to your devices can only be done through an access token. Access token can be easilly gained thorugh the Particle.io [Build](https://build.particle.io/build/) page.
Once on the said page, click on the settings icon on the lower left hand corner of the page. The settings icon is emphazied below:



This will result in your Access token being displyed on the left hand side of the page as demostrated below:

### 3. Start with a Blink:
Once you are familiar with the Particle.io Web IDE, you can go ahead and program your first application for your device. Particle.io provides a basic implimentation of an LED Blink [programme](https://docs.particle.io/guide/getting-started/build/photon/#flashing-your-first-app) to get you started. Once impliemented you will see your Photon/Electron flashing its LED on pin D7. 

### 4. Building and Programming Generic Micro-waggle Code:
Micro-Waggle devices works under a unique design in which they read and publish data. The code found [here](https://github.com/waggle-sensor/summer2018/blob/master/microWaggle/integrated/firmware/microWaggle.ino) gives a generic implimentation of a micro-Waggle application. In the same manner you flashed the [Blink App](https://docs.particle.io/guide/getting-started/build/photon/#flashing-your-first-app) on to your device, you can flash the generic micro-Waggle code onto your Device. 

### 5. See Streaming Data from the Sensors: 
After flashing the generic [code](https://github.com/waggle-sensor/summer2018/blob/master/microWaggle/integrated/firmware/microWaggle.ino), you can check the data being published on the Particle.io cloud through the Particle.io [Console](https://console.particle.io/events).  

### 6. Control the Device from your Computer: 
The micro-Waggle platform allows its users to have some control over there devices via the Particle.io cloud. The deviceController modelue enables this facilty.

#### 6.1 Using the Test Node At ANL 
This module can readilly be used through the Particle.io device already set up for testing at Argonne National Labs. The node runs the Generic microWaggle program described above. You can start by following the instructions given [here](https://github.com/waggle-sensor/microWaggle/tree/master/integrated/software/deviceController). Make sure to include the following details when setting up your local Node Configuration:
- Device ID    : 53002a000c51353432383931
- Access token : c9003c4f929c03b67daac131a84b9d3aa3d75e3e
- Use the default Micro-waggle Config: True

You are free to use any appropriate inputs for the rest of the prompts. After setting up your local config file you will have control over the test node set up. Make sure to try out different configurations before moving forward. To seek how the 
Node respons you may visit this [link](https://api.particle.io/v1/devices/events?access_token=c9003c4f929c03b67daac131a84b9d3aa3d75e3e) which publishes the data coming out of the said Node. 

#### 6.2 Using your own Node 



<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/microWaggle/Resources/Controller_Functions.png?token=AYVA9MNuDebJoiPI5wh-vFXBK5SCwNY-ks5bs-WUwA%3D%3D">

These functions will lend you the same device controls made possible through the [Controller](https://github.com/waggle-sensor/summer2018/blob/master/microWaggle/integrated/software/devicecontroller/README.md) module.
 -->



### 7. Get Beehive Publish Credentials:
The micro-Waggle project keeps all its data at Argonnes Beehive Server. Beehives publish credentials can be requested through any of the following Waggle team members:

### 8. Run Relay Server to Send Data to Beehive: 
Particle.io devices can only publish its data to the Particle.io cloud. As such, a separate module is used to send data from the cloud to the Beehive server. The [relayServer](https://github.com/waggle-sensor/summer2018/blob/master/microWaggle/integrated/software/relayServer/README.md) module is designed to manage this task. Before the implimentation of the python module, a directory structure needs to be set up in the following manner:

```bash
├── parentDirectory
│   ├── relay-server.py
│   ├── microWaggleNodes
│   │   ├──Particle_Node_ID_1 
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
│   │   ├──Particle_Node_ID_2 
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
│   │   ├──Particle_Node_ID_3 
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
................
```
For each Particle Device, the Waggle team will provide 3 files named 'node_id', 'Key.pem' and 'Cert.pem' which carry the necessary credentials for the Relay server module to connect to Beehive.

These files should be put under the Unique directories defined by the Particle Device IDs. A real implimentation of the said file structure would look like this:
```bash
├── parentDirectory
│   ├── relay-server.py
│   ├── microWaggleNodes
│   │   ├──53002a000c51353432383931
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
│   │   ├──53002a000c24353432384231
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
│   │   ├──87002a000c51353432383931
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
................
```
Once the defined file sturture is set up, you can run the following command to send the appropriate data to Beehive. 
```python3 relay-server.py microWaggleNodes```

### 9. Check Data from Device: 
Once the previous command is ran, in less than 5 minutes you should see Microwaggle data being published on [Beehive](https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php). The data will come under the link label: MWTesting.complete.recent.csv.

### 10. Tweak the Micro-Waggle behavior and see changes on Beehive: 

At this point you are in a position to modify the generic microWaggle [code](https://github.com/waggle-sensor/summer2018/blob/master/microWaggle/integrated/firmware/microWaggle.ino) and flash it into your Particle.io devices. After such changes are made, you can observe its effects through [Beehive](https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php). 

### 11. Code your own micro-Waggle Device:

Congradulations, you are ready to impliment your own microWaggle implimentation.

------------------------------------------------------------

#### Helpful Resources:
- [Photon Documentation](https://docs.particle.io/guide/getting-started/examples/photon/).
- [Electron Documentation](https://docs.particle.io/guide/getting-started/examples/electron/).




