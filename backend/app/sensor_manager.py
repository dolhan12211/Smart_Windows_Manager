import datetime
import logging

logger = logging.getLogger(__name__)

from .window import Window # Import Window class

class SensorManager:
    def __init__(self, num_windows=3): # max_entries is no longer directly used for historical data
        self.windows = []
        self.current_window_data = {} # Stores the latest data for each window
        logger.info(f"SensorManager initialized with {num_windows} windows.")

        # Create Window instances
        for i in range(num_windows):
            window_id = f"window_{i+1:03d}"
            window = Window(window_id, self) # Pass self (SensorManager) to Window
            self.windows.append(window)
            self.current_window_data[window_id] = {} # Initialize empty dict for this window's data
            logger.info(f"Created Window {window_id}")

    def get_total_windows(self):
        return len(self.windows)

    def add_data(self, data):
        # This method is called by Window instances to push their latest sensor data
        window_id = data.get("window_id")
        sensor_id = data.get("sensor_id")
        if window_id and sensor_id:
            # Store only the latest reading for each sensor within its window
            self.current_window_data[window_id][sensor_id] = data
            logger.debug(f"Updated latest data for {window_id}/{sensor_id}: {data['value']}")
        else:
            logger.warning(f"Received data without window_id or sensor_id: {data}")

    def get_latest_readings(self):
        # Consolidate and return the latest readings from all windows
        all_latest_data = []
        for window_obj in self.windows: # Iterate through actual Window objects
            window_id = window_obj.window_id
            window_summary = {
                "window_id": window_id,
                "window_open": window_obj.window_open,
                "manual_control_enabled": window_obj.manual_control_enabled,
                "alarm_active": window_obj.alarm_active,
                "sensors": []
            }
            # Add latest sensor data for this window
            sensors_data = self.current_window_data.get(window_id, {})
            for sensor_id, data in sensors_data.items():
                window_summary["sensors"].append(data)
            all_latest_data.append(window_summary)
        logger.debug("Retrieving latest consolidated data.")
        return all_latest_data

    def clear_data(self):
        # Clear all current data
        self.current_window_data = {window_id: {} for window_id in self.current_window_data}
        logger.info("All current sensor data cleared.")

    def get_window_by_id(self, window_id: str):
        for window in self.windows:
            if window.window_id == window_id:
                return window
        return None
