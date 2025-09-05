# utils/websocket_client.py
import websocket
import json
import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal


class PersistentWebSocketClient(QObject):
    """Persistent WebSocket client that maintains connection for chat session"""
    message_received = pyqtSignal(dict)
    connection_status_changed = pyqtSignal(str, str)
    error_occurred = pyqtSignal(str)

    def __init__(self, sender_username):
        super().__init__()
        self.sender_username = sender_username
        self.ws = None
        self.connected = False
        self.keep_running = True
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

    def connect(self, receiver_username=None):
        """Connect to WebSocket server"""
        if self.connected:
            return True

        try:
            websocket_server_uri = "ws://localhost:8000"
            print(f"Connecting to WebSocket server: {websocket_server_uri}")

            self.ws = websocket.WebSocketApp(
                websocket_server_uri,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )

            self.receiver_username = receiver_username
            self.connection_status_changed.emit(
                "connecting", "Connecting to server...")

            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()

            timeout = 5
            start_time = time.time()

            while (time.time() - start_time) < timeout and not self.connected:
                time.sleep(0.1)

            return self.connected

        except Exception as e:
            print(f"WebSocket connection error: {e}")
            self.error_occurred.emit(f"Connection error: {str(e)}")
            return False

    def on_open(self, ws):
        """Handle connection opening"""
        print("WebSocket connection opened successfully")
        self.connected = True
        self.reconnect_attempts = 0
        self.connection_status_changed.emit("connected", "Connected to server")

    def on_message(self, ws, message):
        """Handle incoming messages"""
        try:
            data = json.loads(message)
            print(f"Received WebSocket message: {data}")
            self.message_received.emit(data)

        except json.JSONDecodeError:
            error_msg = "Invalid response format from server"
            print(error_msg)
            self.error_occurred.emit(error_msg)

    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"WebSocket error: {error}")
        self.connected = False
        self.error_occurred.emit(str(error))

    def on_close(self, ws, close_status_code, close_msg):
        """Handle connection closure"""
        print(f"WebSocket connection closed: {
              close_status_code} - {close_msg}")
        self.connected = False
        self.connection_status_changed.emit(
            "disconnected", "Disconnected from server")

        if self.keep_running and self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            print(f"Attempting to reconnect ({
                  self.reconnect_attempts}/{self.max_reconnect_attempts})")
            time.sleep(2)  # Wait before reconnecting
            self.connect(self.receiver_username)

    def send_message(self, receiver_username, message):
        """Send a message through the WebSocket connection"""
        if not self.connected or not self.ws:
            print("Cannot send message - not connected to server")
            self.error_occurred.emit("Not connected to server")
            return False

        try:
            message_data = {
                "sender": self.sender_username,
                "receiver": receiver_username,
                "message": message
            }
            self.ws.send(json.dumps(message_data))
            print(f"Message sent to {receiver_username}: {message}")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            self.error_occurred.emit(f"Error sending message: {str(e)}")
            return False

    def close(self):
        """Close the WebSocket connection"""
        self.keep_running = False
        if self.ws:
            self.ws.close()
        self.connected = False
