# Volvo2evcc
This component is based on Volvo2MQTT and creates a REST service that can be used for evcc vehicle data. This is only needed if the evcc volvo implementation does not fit your car (e.g. new electric models, that only support api version 2). This version implements the OTP login, like the original VOLVO App does, to access volvo electric vehicle API v2.
<p>

<b>Important note: The Volvo api currently ONLY works in these [countries](https://developer.volvocars.com/terms-and-conditions/apis-supported-locations/)</b>

## OTP Authentication

As of version <b>v1.9.0</b>, this addon uses the same OTP authentication as the Volvo app. 
The following steps are required for authentication in exactly this order:

1. Setup volvo2evcc, by checking out this repository
2. Enter your settings into settings.json and start volvo2evcc with Python3 (python3 volvo2evcc.py)
3. The script logs in using your credentials from settings.json and an e-mail to your VOLVO ID mail should be generated
4. Now, open your mailbox and copy your OTP Code
5. Paste the OTP code to the prompt on the command line
6. Now the script should be running and you can send the process to the background by typing ^Z bg and close the terminal


## evcc setup
<b>evcc.yaml:</b>
This example assumes that the service is running on `192.168.0.1` port `8182`. Your VIN is used to distingiush different cars, in case that you have multiple cars registered with your VOLVO ID. So please replace "YOUR_VIN" with the correct VIN, even if you have only one car.
```
vehicles:
- type: custom
  title: My VOLVO
  name: ev5
  capacity: 83
  soc:
    source: http 
    uri: http://192.168.0.1:8182/data
    method: GET
    jq: .data.YOUR_VIN.battery_charge_level 
  range:
    source: http
    uri: http://192.168.0.1:8182/data
    method: GET
    jq: .data.YOUR_VIN.electric_range 
  odometer:
    source: http
    uri: http://192.168.0.1:8182/data
    method: GET
    jq: .data.YOUR_VIN.odometer
```

### TODOs
* URL and PORT is currently hardcoded in main.py - Please change it there to your needs.
* Cleanup code and configs from mqtt code

<b>NOTE: This is the first version, currently tested with my car. Working so far, but still in ALPHA status</b>
