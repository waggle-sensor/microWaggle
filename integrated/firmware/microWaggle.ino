#include <vector>
#include <map>

class Sensor
{
    private:
        int sensingFrequency = 20; //the frequency of sensing
        int lastSensingTime = 0;
        bool enabled = true;
        int sensorId;
        String sensorName;
        int sensorType;

    public:
        Sensor(int id, String name){
            sensorId = id;
            sensorName = name;
        }
        int getSensorId(){
            return sensorId;
        }

        String getSensorName(){
            return sensorName;
        }

        void setSensorId(int id)
        {
            sensorId = id;
        }

        int getSensingFrequency(){
            return sensingFrequency;
        }

        void setSensingFrequency(int newSensFreq){
            sensingFrequency = newSensFreq;
        }

        void setType(int type){
            sensorType= type;
        }


        bool getEnabled(){
            return enabled;
        }

        void setEnabled(bool newEnabled){
            enabled = newEnabled;
        }

        int getLastSensingTime()
        {
            return lastSensingTime;
        }

        int getType(){
            return sensorType;
        }


        void setLastSensingTime(int t)
        {
            lastSensingTime = t;
        }

};
Sensor* tempSensor;
Sensor* humiditySensor;
Sensor* sensorsPtrs[2]; // holds sensor
std::map<int, Sensor*> sensorIdMap;

bool sdCardEnabled = false;
int reportingFreq =10; //60 seconds is default for reporting (sending sensorgrams to cloud)
String status = "";
// thresholdSensorFreq is the lowest sensing frequency that a sensor can have, anything lower is not permitted
int thresholdSensorFreq = 5; //TODO: set this to what Raj feels is good

// **SENSORGRAM VARIABLES**
String allSensorgrams; //stores all the sensorgrams appended on to each other. this is what will be published by particle.publish(...);

int lastSendTime  = Time.now();
int lastStatusTime = Time.now();
int statusFreq = 60;
int maxPublishingLength = 255; // indicates the max amt of characters that you can send in a Particle.publish() call (it is actually around 620, but it's 100 for now for testing)

void setup() {
    sensorIdMap.insert(std::make_pair(1, new Sensor(1, "tempSensor")));
    sensorIdMap.insert(std::make_pair(2, new Sensor(2, "humiditySensor")));

    sensorsPtrs[0] = sensorIdMap[1];
    sensorsPtrs[1] = sensorIdMap[2];
    Particle.function("sensorConfig", sensorConfig);
    Particle.function("nodeConfig", nodeConfig);
}

void loop() {
    // ** some dummy data for the sensorgram testing **
    unsigned short sensorId = 6;
    unsigned char sensor_instance = 70;
    unsigned char param_id = 9;
    uint16_t data = 5;

    // check if time to send status msg
    if (Time.now() - lastStatusTime >= statusFreq)
    {
        status = getStatusMsg();
        Particle.publish("microWaggleStatus", status, PRIVATE);
        lastStatusTime = Time.now();
    }

    // check if time to report the sensorgrams (send sensorgrams)
    if(Time.now() - lastSendTime >= reportingFreq) //time to send/create sensorgram
    {
        lastSendTime = Time.now();
        if(Particle.connected() && allSensorgrams.length() != 0) // particle is connected and atleast one sensorgram is there
            PublishData();
    }

    // check if time to measure with sensor
    for(Sensor *s : sensorsPtrs)
    {
        if((s->getEnabled() == true) && (Time.now() - s->getLastSensingTime() > s->getSensingFrequency())) // time to sense with sensor
        {
            s->setLastSensingTime(Time.now()); //update last sensing time
            String sensorgram = pack((unsigned short)(s->getSensorId()), sensor_instance, param_id, data, s->getLastSensingTime()); // just some dummy data
            allSensorgrams += sensorgram;
            if(allSensorgrams.length() >= maxPublishingLength-15) // if too much of sensorgrams build up, we put a semicolon to indicate that for the next publish, we only send till the semicolon (so we don't send too much in one send)
                allSensorgrams += ";";
        }
    }
}



String getStatusMsg()
{
    String status = "";
    for(Sensor *s : sensorsPtrs)
    {
        String sensorMsg = String(s->getSensorId()) + ":" + s->getSensorName() + "," + boolToEnabledDisabled(s->getEnabled()) + "," + s->getSensingFrequency(); //e.g. format = 01:tempSensor,en,30
        status += sensorMsg + ";";
    }
    status += "SD:" + boolToEnabledDisabled(sdCardEnabled) + ";";
    status += "ReportFreq:" + String(reportingFreq);
    status += "StatusFreq:" + String(statusFreq);
    return status;
}

//returns "en" if true, and "dis" if false
String boolToEnabledDisabled(bool b)
{
    if(b)
        return "en";
    else
        return "dis";
}

// Function to check if the key is present or not
bool check_key(int key)
{
    // Key is not present
    if (sensorIdMap.find(key) == sensorIdMap.end())
        return false;

    return true;
}

int sensorConfig(String param)
{
    int index1 = param.indexOf(";");
    int index2 = param.lastIndexOf(";");

    //TODO: Check for invalid input (i.e., message is not in right format like this "id;status;freq")
    //checking if only 1 semi colon is in param or if there is no semicolon
    if(index1 == index2 || index1 == -1 || index2 == -1) //how do i throw an error message?
        Particle.publish("ERROR", "sensorConfig(): invalid input - data format must be 'id;status;freq'");

    int sensorId = param.substring(0,index1).toInt();
    String sensorStatus = param.substring(index1+1, index2);
    String freq = param.substring(index2+1); // if we don't want to fix frequency, put an _

    bool isSensorIdValid = check_key(sensorId); //checks if inputted sensorId is an existing sensorId
    if(!isSensorIdValid)
        Particle.publish("ERROR", "sensorConfig(): inputted sensorId does not exist");

    if(sensorStatus == "en")
        sensorIdMap[sensorId]->setEnabled(true);
    else if(sensorStatus == "dis")
        sensorIdMap[sensorId]->setEnabled(false);
    if(freq != "_" && freq.toInt() >= thresholdSensorFreq) // if freq is not a num, then freq.toInt() returns 0
        sensorIdMap[sensorId]->setSensingFrequency(freq.toInt());

    return 0;
}



int nodeConfig(String param) {
    param = param.toLowerCase();
    if (param == "enableall") {
        for (Sensor *s : sensorsPtrs) {
            s->setEnabled(true);
        }
    }
    else if (param == "disableall") {
        for (Sensor *s : sensorsPtrs) {
            s->setEnabled(false);
        }
    }
    else if (param == "enablesd") {
        sdCardEnabled = true;
    }
    else if (param == "disablesd") {
        sdCardEnabled = false;
    }

    else if (param.indexOf("statusfreq-") != -1) {

        int statusFrequency = param.substring(11).toInt(); // * if inputted freq of reporting is not a num, inputReportFreq = 0 (.toInt() returns 0)

        if (statusFrequency<5)  // cannot change freq
            Particle.publish("ERROR", "nodeConfig(): requested status frequency of " + param.substring(11) + " seconds is too low. Must be greater than 5 seconds.");
        else
             statusFreq = statusFrequency;
    }


    else if (param.indexOf("freqreport-") != -1) {

        int inputReportFreq = param.substring(11).toInt(); // * if inputted freq of reporting is not a num, inputReportFreq = 0 (.toInt() returns 0)
        int minSensing = inputReportFreq; //minimum possible reporting frequency allowed --> based on the max sensor sensing freq
        bool canChangeFreq = true; // can the reporting frequency be changed?

        for (Sensor *s : sensorsPtrs) {
            if (s->getSensingFrequency() > minSensing) // a sensor sensingFreq is > the requested reporting frequency --> this is bad...
            {
                canChangeFreq = false;
                minSensing = s->getSensingFrequency();
            }
        }
        if (canChangeFreq == false)  // cannot change freq
            Particle.publish("ERROR", "nodeConfig(): requested frequency of " + param.substring(11) + " seconds is too low. Must be greater than " + (minSensing) + " seconds.");
        else
            reportingFreq = inputReportFreq;
    }


    else
        Particle.publish("ERROR", "nodeConfig: command not found");
    return 0;
}



// ****SENSORGRAM FUNCTIONS*****

// publish sensorgram data
void PublishData()
{

        int delimiterIndex = allSensorgrams.indexOf(";");
        String sendData;
        if(delimiterIndex != -1){ // if delimeter exists, then only send up till the delimeter (b/c delimeter indicates the max amount you can send in one publish)
            sendData = allSensorgrams.substring(0, delimiterIndex); //TODO: Check if this works correctly...
            allSensorgrams = allSensorgrams.substring(delimiterIndex+1); // set allSensorgrams to everything after the first semi colon
        }
        else // no delimeter, so just send all that we have right now
            sendData = allSensorgrams;
   if(sendData.length()>1){
        Particle.publish("sensorgram", sendData, PRIVATE);
    }
}

String pack(unsigned short sensorID, unsigned char sensor_instance, unsigned char parameter_id,  uint16_t data, unsigned int cTime) {

	String sensorIDHex = ShortToHex(sensorID);
	String sensorInstanceHex = CharToHex(sensor_instance);
	String parameterIdHex = CharToHex(parameter_id);
	String dataHex = Int_16_to_Hex(&data);
	String cTimeHex = IntToHex(cTime);
  String type = "15";
  String lengthOfData = "0002";
	String sensorgramString = lengthOfData + sensorIDHex + sensorInstanceHex + parameterIdHex +  cTimeHex + type +dataHex+";";

	// [Length (2B)] [Sensor_ID (2B)] [Sensor_Instance (1B)] [Parameter_ID (1B)] [ Sampling_Time (4B)] [ Data_Format (1B)] [data (xB)]
    return sensorgramString;
}


String IntToHex(unsigned int number)
{
	byte chars[4];
	byte* a_begin = reinterpret_cast<byte*>(&number);
	for (int i = 0; i < 4; i++)
		chars[3-i] = a_begin[i]; //add it in reverse for big endian
	return BytearrayToHex(chars, 4);
}


String ShortToHex(unsigned short number)
{
	byte chars[2];
	byte* a_begin = reinterpret_cast<byte*>(&number);
	for (int i = 0; i < 2; i++)
		chars[1 - i] = a_begin[i]; //add it in reverse for big endian

	return BytearrayToHex(chars, 2);
}


String CharToHex(unsigned char number)
{
	byte chars[1];
	byte* a_begin = reinterpret_cast<byte*>(&number);
	chars[0] = *a_begin;
	return BytearrayToHex(chars, 1);
}


String BytearrayToHex(byte* bytearray, int length) {
	//convert to hex String
	String hexStr = "";
	for (int i = 0; i < length; i++)
	{
		char temp[4]; //always 4
		sprintf(temp, "%02x", (byte)bytearray[i]);
		hexStr = hexStr + temp;
	}
	return hexStr;
}


String Int_16_to_Hex(uint16_t* yourint16_t){
unsigned char ch[4];
memcpy(ch,yourint16_t,sizeof(uint16_t));
String Final= Char_Byte_2_Hex(ch[1])+ Char_Byte_2_Hex(ch[0]);
return Final;
}


String Char_Byte_2_Hex(char val){

      String Zeros = "00";
      String Hex = String(int(val),HEX);
      String Final;

    if (Hex.length()<Zeros.length())
        {
        Final  =  Zeros.substring(0,Zeros.length()-Hex.length())+Hex;
        }
        else{
        Final =  Hex;

        }

    return Final;

}
