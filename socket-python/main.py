import socketio
import logging
from acknowledge_message import get_acknowledge_message
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
sio = socketio.Client(logger=True)

ROOT_URL = 'https://api.fruitful.ag'
SYSTEM_ID = os.environ['SYSTEM_ID']
DEVICE_ID = os.environ['DEVICE_ID']
X_API_KEY = os.environ['X_API_KEY']

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

  data = get_acknowledge_message(message=message)
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

  data = get_acknowledge_message(message=message)
  logger.info(f'Emitting: {data}')
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
  data = get_acknowledge_message(message=message)

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

sio.wait()
