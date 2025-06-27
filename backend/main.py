import logging
import time
import atexit
import os

# Configure logging for the main script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import components from the app directory
# Assuming main.py is now in 'backend/' and app components are in 'backend/app/'
from app.api_app import app, set_sensor_manager
from app.sensor_manager import SensorManager
from app.data_generator import DataGenerator

if __name__ == "__main__":
    logger.info("Starting application orchestration...")

    # Initialize SensorManager
    sensor_manager = SensorManager()
    logger.info("SensorManager initialized.")

    # Initialize DataGenerator and start data generation (conditionally)
    data_generator = None
    if os.getenv("RUN_DATA_GENERATOR", "false").lower() == "true":
        data_generator = DataGenerator(sensor_manager)
        data_generator.start_generation()
        logger.info("Data generation started by DataGenerator.")
    else:
        logger.info("Data generation skipped. Expecting external data input.")

    # Pass the sensor_manager instance to the api_app
    set_sensor_manager(sensor_manager)

    # Start the Flask app
    logger.info("Starting Flask API application...")
    app.run(host="0.0.0.0", port=8000, debug=True)
