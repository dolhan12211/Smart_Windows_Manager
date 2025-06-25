import React from 'react';

function SensorDisplay({ sensor }) {
  const { sensor_id, sensor_type, value, unit, timestamp } = sensor;

  const formatValue = () => {
    if (sensor_type === 'motion') {
      return value ? 'Detected' : 'Not Detected';
    }
    if (sensor_type === 'alarm_status' || sensor_type === 'window_status') {
      return value.toUpperCase();
    }
    return `${value} ${unit}`;
  };

  const statusColorClass = () => {
    if (sensor_type === 'window_status') {
      return value === 'open' ? 'text-green-500' : 'text-red-500';
    }
    if (sensor_type === 'alarm_status') {
      return value === 'active' ? 'text-red-500' : 'text-green-500';
    }
    if (sensor_type === 'motion' && value) {
      return 'text-red-500 font-bold'; // Highlight motion detection
    }
    if (sensor_type === 'temperature') {
      if (value > 28 || value < 12) { // Example thresholds for extreme temperature
        return 'text-red-500 font-bold';
      }
    }
    if (sensor_type === 'humidity') {
      if (value > 65 || value < 35) { // Example thresholds for extreme humidity
        return 'text-red-500 font-bold';
      }
    }
    return 'text-gray-300'; // Default for other sensors
  };

  const motionHighlightClass = (sensor_type === 'motion' && value) ? 'bg-red-900 border-red-500' : '';

    return (
      <div className={`bg-gray-800 border border-gray-700 p-2 rounded-md text-xs ${motionHighlightClass}`}>
        <p className="text-blue-400 font-bold">{sensor_type.replace('_', ' ').toUpperCase()}</p>
        <p>ID: <span className="text-blue-300">{sensor_id}</span></p>
        <p>Value: <span className={`font-semibold ${statusColorClass()}`}>{formatValue()}</span></p>
        <p className="text-gray-500 text-xs">
          {new Date(timestamp).toLocaleString('pl-PL', { timeZone: 'Europe/Warsaw', hour: '2-digit', minute: '2-digit', second: '2-digit' })}
        </p>
      </div>
    );
  }

export default SensorDisplay;
