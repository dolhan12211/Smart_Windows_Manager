import React from 'react';
import SensorDisplay from './SensorDisplay';

function WindowCard({ windowData }) {
  const { window_id, sensors, window_open, manual_control_enabled, alarm_active } = windowData;

  const windowStatusClass = window_open ? 'text-green-400' : 'text-red-400';
  const windowStatusText = window_open ? 'OPEN' : 'CLOSED';
  const manualControlClass = manual_control_enabled ? 'bg-yellow-600' : 'bg-gray-600';
  const manualControlText = manual_control_enabled ? 'MANUAL ON' : 'MANUAL OFF';
  const alarmStatusClass = alarm_active ? 'text-red-500' : 'text-green-500';
  const alarmStatusText = alarm_active ? 'ACTIVE' : 'INACTIVE';


  const sendCommand = async (endpoint, body = {}) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/${endpoint}/${window_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log(`Command ${endpoint} for ${window_id} successful:`, result);
    } catch (error) {
      console.error(`Error sending command ${endpoint} for ${window_id}:`, error);
    }
  };

  const toggleManualControl = () => {
    sendCommand('set_manual_control', { enable: !manual_control_enabled });
  };

  const handleOpenWindow = () => {
    sendCommand('open_window');
  };

  const handleCloseWindow = () => {
    sendCommand('close_window');
  };

  const handleActivateAlarm = () => {
    sendCommand('activate_alarm');
  };

  const handleDeactivateAlarm = () => {
    sendCommand('deactivate_alarm');
  };

  return (
    <div className="bg-gray-900 border border-blue-500 p-4 rounded-lg shadow-lg flex flex-col space-y-4">
      <h3 className="text-xl font-bold text-blue-400">{window_id.replace('_', ' ').toUpperCase()}</h3>
      <p className={`text-lg font-semibold ${windowStatusClass}`}>Window Status: {windowStatusText}</p>
      <p className={`text-lg font-semibold ${alarmStatusClass}`}>Alarm: {alarmStatusText}</p>

      <button
        onClick={toggleManualControl}
        className={`py-2 px-4 rounded-md text-white font-semibold ${manualControlClass} hover:opacity-80 transition-opacity`}
      >
        {manualControlText}
      </button>

      {manual_control_enabled && (
        <div className="flex flex-col space-y-2">
          <button
            onClick={handleOpenWindow}
            className="bg-green-500 py-2 px-4 rounded-md text-white font-semibold hover:bg-green-600"
          >
            Open Window
          </button>
          <button
            onClick={handleCloseWindow}
            className="bg-red-500 py-2 px-4 rounded-md text-white font-semibold hover:bg-red-600"
          >
            Close Window
          </button>
          <button
            onClick={handleActivateAlarm}
            className="bg-orange-500 py-2 px-4 rounded-md text-white font-semibold hover:bg-orange-600"
          >
            Activate Alarm
          </button>
          <button
            onClick={handleDeactivateAlarm}
            className="bg-purple-500 py-2 px-4 rounded-md text-white font-semibold hover:bg-purple-600"
          >
            Deactivate Alarm
          </button>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        {sensors.map((sensor, index) => (
          <SensorDisplay key={index} sensor={sensor} />
        ))}
      </div>
    </div>
  );
}

export default WindowCard;
