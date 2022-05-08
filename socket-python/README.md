# Connect to Fruitful via Sockets

### Goal

Receive commands from the [Fruitful Portal](https://app.fruitful.ag) to control lights, relays, pumps, etc.

-----------------------

### Description of socket topics

You can listen to a set of socket topics - each topic has a metadata payload attached:

 - `get_control_status`
    - This is triggered when the user requests the current status of 
    your control. For example, this is used to request whether a light is on or off. 
 - `set_control_status`
    - This is triggered when the user requests a state change on client side. For example, this is used when the user requests to either turn a light is on or off.  
 - `set_control_schedule`
   - This is is triggered when the user requests to set a schedule for your control. For example, this is used to set a scheule for a light (10h on, 14h off - recurrent schedule)
 - `client_error`
   - This is triggered when a 4xx error happens on server side. 

### Example payload for the `set_control_status` topic
```python
{
  "deviceId": "my_device_id", # ID of device requesting a state change
  "name": "My Light", # Name of control
  "topic": "set_control_status", # Name of socket topic
  "gpio_channel": 22, # GPIO Channel where control is connected to
  "deviceType": "ESP32 Lights Relay", # Type of device                      
  "systemId": "XLl5fxbMjaUfP1dnsVum", # System where this device is connected to
  "controlId": "jWkpIjY3lrl6cmMtU6P8", # Unique ID of control 
  "gpioStatus": True, # True -> relay=ON, False -> relay=OFF
  "clientDeviceStatusType": "set_relay_light_schedule", 
  "startTime": 1651997479381, # Milliseconds since epoch (UTC)
  "lightDurationInHours": 0, # Duration of light schedule
  "automaticMode": True, # Whether or not this schedule should be recurrent
  "started_by": "user" # Who initiated the command (user / rule based / AI)
}

```