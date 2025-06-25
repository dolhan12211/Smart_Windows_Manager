import logging
import threading
import atexit
import time
from .sensor_manager import SensorManager
from .window import Window # Import Window class

logger = logging.getLogger(__name__)

class DataGenerator:
    def __init__(self, sensor_manager: SensorManager):
        self.sensor_manager = sensor_manager
        self._stop_event = threading.Event()
        logger.info("DataGenerator initialized.")

    def start_generation(self):
        logger.info("Starting data generation from all windows.")
        for window in self.sensor_manager.windows:
            window.start() # Start each window's thread
            logger.info(f"Window {window.window_id} thread started by DataGenerator.")
        atexit.register(self.stop_generation) # Register stop on exit

    def stop_generation(self):
        logger.info("Stopping data generation from all windows.")
        for window in self.sensor_manager.windows:
            window.stop()
            window.join() # Wait for the thread to finish
            logger.info(f"Window {window.window_id} thread stopped.")
        self._stop_event.set()
        logger.info("DataGenerator stopped.")
