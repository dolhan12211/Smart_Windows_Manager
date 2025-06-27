from dotenv import load_dotenv
load_dotenv()

import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import threading
import atexit

from .sensor_manager import SensorManager
from .window import Window # Import Window class to use in type hints and for clarity
from .action_logger import log_action # Import the custom action logger
from .auth import authenticate_user, create_token, token_required, register_user # Import authentication functions

# DataGenerator is now orchestrated by main.py, so no direct import/init here
# from .data_generator import DataGenerator 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static/static')

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # Allow frontend development server
    "http://127.0.0.1:3000", # Allow frontend development server when accessed via 127.0.0.1
    "http://4.233.221.95:3000", # Allow frontend when accessed via Azure VM public IP
]
CORS(app, resources={r"/*": {"origins": origins}})

# SensorManager will be passed from main.py
sensor_manager_instance = None 

def set_sensor_manager(sm: SensorManager):
    global sensor_manager_instance
    sensor_manager_instance = sm
    logger.info("SensorManager instance set in api_app.")

def get_window_or_404(window_id: str) -> Window:
    window = sensor_manager_instance.get_window_by_id(window_id)
    if not window:
        return jsonify({"status": "error", "message": f"Window {window_id} not found"}), 404
    return window

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    if data:
        sensor_manager_instance.add_data(data)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify(sensor_manager_instance.get_latest_readings())

@app.route("/clear_data", methods=["POST"])
def clear_data():
    sensor_manager_instance.clear_data()
    return jsonify({"status": "data cleared"})

@app.route("/command", methods=["POST"])
def receive_command():
    command_data = request.get_json()
    command = command_data.get("command")
    if command:
        log_action(f"Received command: {command}") # Log this action
        return jsonify({"status": "command received", "command": command})
    return {"status": "error", "message": "No command provided"}

@app.route("/login", methods=["POST"])
def login():
    auth_data = request.get_json()
    username = auth_data.get("username")
    password = auth_data.get("password")

    if not username or not password:
        log_action(f"API: Login attempt failed - missing credentials for username: {username}")
        return jsonify({"message": "Username and password are required!"}), 400

    if authenticate_user(username, password):
        token = create_token(username)
        log_action(f"API: User {username} logged in successfully.")
        return jsonify({"token": token}), 200
    else:
        log_action(f"API: Login attempt failed - invalid credentials for username: {username}")
        return jsonify({"message": "Invalid credentials!"}), 401

@app.route("/register", methods=["POST"])
def register():
    user_data = request.get_json()
    username = user_data.get("username")
    password = user_data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    success, message = register_user(username, password)
    if success:
        log_action(f"API: User {username} registered successfully.")
        return jsonify({"message": message}), 201
    else:
        log_action(f"API: Registration attempt failed for username: {username} - {message}")
        return jsonify({"message": message}), 409 # Conflict

@app.route("/set_manual_control/<window_id>", methods=["POST"])
@token_required
def set_manual_control(current_user: str, window_id: str):
    window = get_window_or_404(window_id)
    if isinstance(window, tuple): # Check if it's an error response
        return window
    
    enable = request.get_json().get("enable")
    if enable is None:
        return jsonify({"status": "error", "message": "Missing 'enable' parameter"}), 400
    
    window.set_manual_control(enable)
    log_action(f"API: User {current_user} set manual control for {window_id} to {enable}") # Log this action
    return jsonify({"status": "ok", "window_id": window_id, "manual_control_enabled": enable})

@app.route("/open_window/<window_id>", methods=["POST"])
@token_required
def open_window_manual(current_user: str, window_id: str):
    window = get_window_or_404(window_id)
    if isinstance(window, tuple):
        return window
    
    window.open_window()
    log_action(f"API: User {current_user} manually opened window {window_id}") # Log this action
    return jsonify({"status": "ok", "window_id": window_id, "window_open": window.window_open})

@app.route("/close_window/<window_id>", methods=["POST"])
@token_required
def close_window_manual(current_user: str, window_id: str):
    window = get_window_or_404(window_id)
    if isinstance(window, tuple):
        return window
    
    window.close_window()
    log_action(f"API: User {current_user} manually closed window {window_id}") # Log this action
    return jsonify({"status": "ok", "window_id": window_id, "window_open": window.window_open})

@app.route("/activate_alarm/<window_id>", methods=["POST"])
@token_required
def activate_alarm_manual(current_user: str, window_id: str):
    window = get_window_or_404(window_id)
    if isinstance(window, tuple):
        return window
    
    window.activate_alarm("Manual activation via API")
    log_action(f"API: User {current_user} manually activated alarm for {window_id}") # Log this action
    return jsonify({"status": "ok", "window_id": window_id, "alarm_active": window.alarm_active})

@app.route("/deactivate_alarm/<window_id>", methods=["POST"])
@token_required
def deactivate_alarm_manual(current_user: str, window_id: str):
    window = get_window_or_404(window_id)
    if isinstance(window, tuple):
        return window
    
    window.deactivate_alarm()
    log_action(f"API: User {current_user} manually deactivated alarm for {window_id}") # Log this action
    return jsonify({"status": "ok", "window_id": window_id, "alarm_active": window.alarm_active})

# Serve static files for the React app
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.root_path, app.static_folder, path)):
        return send_from_directory(os.path.join(app.root_path, app.static_folder), path)
    else:
        return send_from_directory(os.path.join(app.root_path, app.static_folder), 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
