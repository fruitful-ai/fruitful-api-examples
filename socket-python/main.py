import socketio
import logging
from typing import Dict

logger = logging.getLogger(__name__)
sio = socketio.Client(logger=True)

ROOT_URL = 'https://api-dev.fruitful.ag'
SYSTEM_ID = '<SYSTEM_ID>'
DEVICE_ID = '<DEVICE_ID>' 
X_API_KEY = '<X_API_KEY>'

sio.connect(
  url=f'{ROOT_URL}?systemId={SYSTEM_ID}&deviceId={DEVICE_ID}', 
  auth={"X-API-KEY": X_API_KEY},
  namespaces='/command',
)

@sio.on('get_control_status', namespace='/command')
def get_control_status(message) -> None:
  """Gets the status of control (controlId), including all schedules for 
  light, pumps, etc. set on client side.

  This function _must_ emit an event containing the current status of the control.

  Args:
      message (Dict): Dict containing instructions received from Fruitful Portal
  """
  logger.info(f'Received message: {message}')

  data = _get_acknowledge_message(message=message)
  sio.emit('client_device_info', data, namespace='/command') 

@sio.on('set_control_status', namespace='/command')
def set_control_status(message) -> None:
  """Sets the status of control (controlId), including all schedules for 
  light, pumps, etc. set on client side.

  This functions emits an event containing the current status of the device

  Args:
      message (Dict): Dict containing instructions received from Fruitful Portal
  """
  logger.info(f'Received message: {message}')

  # TODO: Switch relay on / off based on incoming message
  gpio_status = message.get('gpioStatus', False)

  data = _get_acknowledge_message(message=message)
  sio.emit('client_device_info', data, namespace='/command') 

@sio.on('set_control_schedule', namespace='/command')
def set_control_schedule(message) -> None:
  """Sets a relay pump schedule for this device.

  This functions emits an event containing the current status of the device.

  Args:
      message (Dict): Dict containing instructions received from Fruitful Portal
  """
  logger.info(f'Received message: {message}')

  # TODO: Set pump schedule based on incoming message
  data = _get_acknowledge_message(message=message)
  print(data)

  # Emit acknowledge message
  sio.emit('client_device_info', data, namespace='/command')

@sio.on('client_error', namespace='/command')
def client_error(message) -> None:
  """Server will emit to this socket topic if a 4xx error 
  occurs on server side.

  Args:
      message (Dict): error message from server
  """
  logger.error(f'[ERROR]: {message}')

@sio.on('error', namespace='/command')
def error(message) -> None:
  """Local socket io error listener

  Args:
      message (str): error message
  """
  logger.error(f'[ERROR]: {message}')

def _get_acknowledge_message(message: Dict) -> Dict:
  device_type = message.get('deviceType', None)

  if device_type == 'ESP 32 Relay Pump':
    # Acknowledge current active state of deviceType: ESP 32 Relay Pump
    return _get_esp_32_relay_pump_acknowledge_message(message)
  elif device_type == 'ESP32 Lights Relay':
    # Acknowledge current active state of deviceType: ESP 32 Relay Light
    return _get_esp_32_relay_light_acknowledge_message(message=message)
  else:
    raise ValueError('Unknown device type')

def _get_esp_32_relay_pump_acknowledge_message(message: Dict) -> Dict:
  """Get message to acknowledge events passed to deviceType: ESP 32 Relay Pump.
  Args:
      message (Dict): Dict containing metadata sent from the Fruitful portal
  
  Returns:
      Dict: Dict to be emitted to Fruitful server on success. All keys are required in order to 
      acknowledge a message of deviceType: ESP 32 Relay Pump. 

      PS! The order of the returned keys matter on server side schema validation. 
  """
  control_id = message.get('controlId', None)
  device_type = message.get('deviceType', None)
  automatic_mode = message.get('automaticMode', False)
  pump_interval_in_hours_when_light_is_on = message.get('pumpIntervalInHoursWhenLightIsOn', 0)
  pump_interval_in_hours_when_light_is_off = message.get('pumpIntervalInHoursWhenLightIsOff', 0)
  pump_interval_in_minutes_when_light_is_on = message.get('pumpIntervalInMinutesWhenLightIsOn', 0)
  pump_interval_in_minutes_when_light_is_off = message.get('pumpIntervalInMinutesWhenLightIsOff', 0)
  pump_duration_in_minutes = message.get('pumpDurationInMinutes', 0)
  client_device_status_type = message.get('clientDeviceStatusType', None)
  gpio_channel_status = True # True -> relay=ON, False -> relay=OFF

  return {
    "automatic_mode": automatic_mode, # whether relay schedule is set to automatic or not
    "control_id": control_id, # control id
    "device_type": device_type, # device type
    "gpio_channel_status": gpio_channel_status, # whether relay is currently ON or OFF
    "message": 'Successfully set pump schedule', # customisable textual description of event
    "pump_duration_in_minutes": pump_duration_in_minutes, 
    "pump_interval_in_hours_when_light_is_off": pump_interval_in_hours_when_light_is_off, 
    "pump_interval_in_hours_when_light_is_on": pump_interval_in_hours_when_light_is_on, 
    "pump_interval_in_minutes_when_light_is_off": pump_interval_in_minutes_when_light_is_off, 
    "pump_interval_in_minutes_when_light_is_on": pump_interval_in_minutes_when_light_is_on, 
    "client_device_status_type": client_device_status_type, # type of emitted status - should be set to the same as what is received from fruitful portal
  }

def _get_esp_32_relay_light_acknowledge_message(message: Dict) -> Dict:
  """Get message to acknowledge events passed to deviceType: ESP 32 Relay Light.
  Args:
      message (Dict): Dict containing metadata sent from the Fruitful portal
  
  Returns:
      Dict: Dict to be emitted to Fruitful server on success. All keys are required in order to 
      acknowledge a message of deviceType: ESP 32 Relay Light. 

      PS! The order of the returned keys matter on server side schema validation. 
  """
  start_time = message.get('startTime', 0)
  control_id = message.get('controlId', None)
  device_type = message.get('deviceType', None)
  automatic_mode = message.get('automaticMode', False)
  light_duration_in_hours = message.get('lightDurationInHours', 0)
  light_duration_in_minutes = message.get('lightDurationInMinutes', 0)
  client_device_status_type = message.get('clientDeviceStatusType', None)
  gpio_channel_status = True # True -> relay=ON, False -> relay=OFF

  return {
    "automatic_mode": automatic_mode, # whether relay schedule is set to automatic or not
    "control_id": control_id, # control id
    "device_type": device_type, # device type
    "gpio_channel_status": gpio_channel_status, # whether relay is currently ON or OFF
    "light_duration_in_hours": light_duration_in_hours,
    "light_duration_in_minutes": light_duration_in_minutes,
    "message": f'Setting pump schedule: {start_time}', # customisable textual description of event
    "start_time": start_time, # start time of schedule,
    "client_device_status_type": client_device_status_type,
  }

sio.wait()
