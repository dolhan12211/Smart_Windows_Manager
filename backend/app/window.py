import random
import time
import threading
import logging
import random
import time
import threading
from .sensors import TemperatureSensor, LightSensor, MotionSensor, HumiditySensor
from .action_logger import log_action # Import the custom action logger

logger = logging.getLogger(__name__) # Keep the default logger for sensor data

class Window(threading.Thread):
    def __init__(self, window_id, sensor_manager):
        super().__init__()
        self.window_id = window_id
        self.sensor_manager = sensor_manager
        self.sensors = {
            "temperature": TemperatureSensor(f"temp_{window_id}"),
            "light": LightSensor(f"light_{window_id}"),
            "motion": MotionSensor(f"motion_{window_id}"),
            "humidity": HumiditySensor(f"humidity_{window_id}")
        }
        self.cycle_count = 0
        self.trend = random.choice([-1, 0, 1]) # -1: decreasing, 0: stable, 1: increasing
        self._stop_event = threading.Event()
        self.update_interval = 0.5 # seconds for sensor data generation
        self.check_interval = 2 # seconds for checking thresholds
        self.window_open = True # Initial state of the window
        self.manual_control_enabled = False # New: Manual control flag
        self.alarm_active = False # New: Alarm state
        logger.info(f"Window {self.window_id} initialized with initial trend: {self.trend}")

    def run(self):
        logger.info(f"Window {self.window_id} started its sensor update loop.")
        next_check_time = time.time() + self.check_interval
        while not self._stop_event.is_set():
            self.update_sensors()
            
            if not self.manual_control_enabled and time.time() >= next_check_time:
                self.check_sensors_and_act()
                next_check_time = time.time() + self.check_interval

            time.sleep(self.update_interval)
        logger.info(f"Window {self.window_id} stopped its sensor update loop.")

    def stop(self):
        self._stop_event.set()

    def set_manual_control(self, enable: bool):
        old_state = self.manual_control_enabled
        self.manual_control_enabled = enable
        log_action(f"Window {self.window_id}: Manual control changed from {old_state} to {self.manual_control_enabled}")

    def close_window(self):
        if self.window_open:
            self.window_open = False
            log_action(f"Window {self.window_id}: Window state changed to CLOSED.")
            # In a real scenario, this would send a command to a physical window actuator

    def open_window(self):
        if not self.window_open:
            self.window_open = True
            log_action(f"Window {self.window_id}: Window state changed to OPEN.")
            # In a real scenario, this would send a command to a physical window actuator

    def activate_alarm(self, reason=""):
        if not self.alarm_active:
            self.alarm_active = True
            log_action(f"Window {self.window_id}: ALARM ACTIVATED! Reason: {reason}")
            # In a real scenario, this would activate an alarm system

    def deactivate_alarm(self):
        if self.alarm_active:
            self.alarm_active = False
            log_action(f"Window {self.window_id}: ALARM DEACTIVATED.")

    def check_sensors_and_act(self):
        # Get latest data from sensors
        temp_data = self.sensors["temperature"].get_data()
        light_data = self.sensors["light"].get_data()
        motion_data = self.sensors["motion"].get_data()
        humidity_data = self.sensors["humidity"].get_data()

        # Example thresholds and actions
        if temp_data["value"] > 30:
            self.close_window()
            self.activate_alarm(f"High temperature ({temp_data['value']}°C)")
        elif temp_data["value"] < 10:
            self.open_window() # Open if too cold, assuming it helps regulate
        
        if motion_data["value"] == True:
            if self.alarm_active: # Log motion only if alarm is active
                log_action(f"Window {self.window_id}: Motion detected while alarm is ACTIVE!")
        
        if humidity_data["value"] > 70:
            self.close_window()
            log_action(f"Window {self.window_id}: Closing window due to high humidity ({humidity_data['value']}%)")

        # Update each sensor and send data to SensorManager
    def update_sensors(self):
        self.cycle_count += 1

        # Randomize trend every 100 cycles
        if self.cycle_count % 100 == 0:
            self.trend = random.choice([-1, 0, 1])
            logger.debug(f"Window {self.window_id} trend randomized to: {self.trend}")

        # Update each sensor and send data to SensorManager
        for sensor_type, sensor_obj in self.sensors.items():
            sensor_obj.update_value(trend_direction=self.trend)
            payload = sensor_obj.get_data()
            payload["window_id"] = self.window_id # Add window_id to payload
            payload["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            payload["window_open"] = self.window_open # Add window_open status
            payload["manual_control_enabled"] = self.manual_control_enabled # Add manual_control_enabled status
            payload["alarm_active"] = self.alarm_active # Add alarm_active status
            self.sensor_manager.add_data(payload)
            logger.debug(f"Window {self.window_id} sent {sensor_type} data: {payload['value']}")
