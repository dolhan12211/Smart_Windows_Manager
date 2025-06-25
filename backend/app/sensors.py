import random
import logging

logger = logging.getLogger(__name__)

class BaseSensor:
    def __init__(self, sensor_id, sensor_type, unit, min_range, max_range, default_value):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit
        self.min_range = min_range
        self.max_range = max_range
        self.value = default_value
        logger.debug(f"Initialized {self.sensor_type} {self.sensor_id} with value {self.value}")

    def update_value(self, trend_direction=0, change_magnitude=0.1):
        # Apply trend bias
        if trend_direction > 0: # positive trend
            change = random.uniform(0, change_magnitude)
        elif trend_direction < 0: # negative trend
            change = random.uniform(-change_magnitude, 0)
        else: # no strong trend, random change
            change = random.uniform(-change_magnitude / 2, change_magnitude / 2)

        self.value += change
        self.value = max(self.min_range, min(self.max_range, self.value)) # Keep within range
        logger.debug(f"Updated {self.sensor_type} {self.sensor_id} to {self.value:.2f}")
        return self.value

    def get_data(self):
        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "value": round(self.value, 2),
            "unit": self.unit
        }

class TemperatureSensor(BaseSensor):
    def __init__(self, sensor_id, default_value=22.0):
        super().__init__(sensor_id, "temperature", "celsius", 15.0, 35.0, default_value)

class LightSensor(BaseSensor):
    def __init__(self, sensor_id, default_value=50.0):
        super().__init__(sensor_id, "light", "lux", 0.0, 100.0, default_value)

class HumiditySensor(BaseSensor):
    def __init__(self, sensor_id, default_value=60.0):
        super().__init__(sensor_id, "humidity", "percentage", 30.0, 90.0, default_value)

class MotionSensor(BaseSensor):
    def __init__(self, sensor_id, default_value=False):
        super().__init__(sensor_id, "motion", "boolean", 0, 1, default_value) # 0 for no motion, 1 for motion
        self.value = 1 if default_value else 0 # Store as 0 or 1 internally

    def update_value(self, trend_direction=0, change_magnitude=0): # Motion is binary, not continuous
        if random.random() < 0.05: # 5% chance to toggle state
            self.value = 1 - self.value
            logger.debug(f"Toggled {self.sensor_type} {self.sensor_id} to {bool(self.value)}")
        return self.value

    def get_data(self):
        data = super().get_data()
        data["value"] = bool(self.value) # Return boolean for motion sensor
        return data
