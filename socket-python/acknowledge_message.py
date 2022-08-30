
from typing import Dict
import inflection

def get_acknowledge_message(message: Dict) -> Dict:
  device_type = message.get('deviceType', None)

  if device_type == 'ESP 32 Relay Pump':
    return get_pump_acknowledge_message(message=message)
  elif device_type == 'ESP32 Lights Relay':
    return get_light_acknowledge_message(message=message)
  elif device_type == 'Temperature Controller':
    return get_temperature_controller_acknowledge_message(message=message)
  elif device_type == 'Raspberry Pi v4 Relay':
    return get_pump_acknowledge_message(message=message)
  elif device_type == 'Relay Controller':
    return parse_message_keys(message)
  else:
    raise ValueError('Unknown device type')

def parse_message_keys(message: Dict) -> Dict:
  message_snake_case = {} # API expects keys of the message to be snake_case
  for key in message:
    underscore_key = inflection.underscore(key) 
    message_snake_case[underscore_key] = message[key]

  return message_snake_case

def get_temperature_controller_acknowledge_message(message: Dict) -> Dict:
  message = parse_message_keys(message)
  return message

def get_pump_acknowledge_message(message: Dict) -> Dict:
  """Get message to acknowledge events passed to deviceType: ESP 32 Relay Pump.
  Args:
      message (Dict): Dict containing metadata sent from the Fruitful portal
  
  Returns:
      Dict: Dict to be emitted to Fruitful server on success. All keys are required in order to 
      acknowledge a message of deviceType: ESP 32 Relay Pump. 

      PS! The order of the returned keys matter on server side schema validation. 
  """
  message = {
    "automatic_mode": message.get('automaticMode', False), # whether relay schedule is set to automatic or not
    "control_id": message['controlId'], # control id
    "device_type": message['deviceType'], # device type
    "gpio_channel_status": message.get('gpioStatus', False), # whether relay is currently ON or OFF
    "message": 'Custom Message', # customisable textual description of event
    "pump_duration_in_minutes": message.get('pumpDurationInMinutes', 0), 
    "pump_interval_in_hours_when_light_is_off": message.get('pumpIntervalInHoursWhenLightIsOff', 0),
    "pump_interval_in_hours_when_light_is_on": message.get('pumpIntervalInHoursWhenLightIsOn', 0),
    "pump_interval_in_minutes_when_light_is_off": message.get('pumpIntervalInMinutesWhenLightIsOff', 0),
    "pump_interval_in_minutes_when_light_is_on": message.get('pumpIntervalInMinutesWhenLightIsOn', 0),
    "client_device_status_type": message['clientDeviceStatusType'], # type of emitted status - should be set to the same as what is received from fruitful portal
  }

  return parse_message_keys(message)

def get_light_acknowledge_message(message: Dict) -> Dict:
  """Get message to acknowledge events passed to deviceType: ESP 32 Relay Light.
  Args:
      message (Dict): Dict containing metadata sent from the Fruitful portal
  
  Returns:
      Dict: Dict to be emitted to Fruitful server on success. All keys are required in order to 
      acknowledge a message of deviceType: ESP 32 Relay Light. 

      PS! The order of the returned keys matter on server side schema validation. 
  """
  message = {
    "automatic_mode": message.get('automaticMode', False), # whether relay schedule is set to automatic or not
    "control_id": message['controlId'], # control id
    "device_type": message['deviceType'], # device type
    "gpio_channel_status": message.get('gpioStatus', False), # whether relay is currently ON or OFF
    "light_duration_in_hours": message.get('lightDurationInHours', 0),
    "light_duration_in_minutes": message.get('lightDurationInMinutes', 0),
    "message": 'Setting pump schedule', # customisable textual description of event
    "start_time": message.get('startTime', 1234), # start time of schedule,
    "client_device_status_type": message['clientDeviceStatusType'],
  }
  return parse_message_keys(message)

