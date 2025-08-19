import websocket
import json


def run_websocket_client(sender, receiver, message, on_success, on_error, on_message):
    """Run a WebSocket client to send a message and handle responses."""
    def on_open(ws):
        """Send the message and keep connection open for response."""
        try:
            ws.send(json.dumps(
                {"sender": sender, "receiver": receiver, "message": message}))
        except Exception as e:
            on_error(str(e))

    def on_message_handler(ws, message):
        """Handle incoming messages."""
        try:
            data = json.loads(message)
            on_message(data)
        except json.JSONDecodeError:
            on_error("Invalid response format")
        finally:
            ws.close()

    def on_error_handler(ws, error):
        """Handle WebSocket errors."""
        on_error(str(error))

    def on_close(ws, close_status_code, close_msg):
        """Handle connection closure."""
        pass

    try:
        websocket_server_uri = "ws://localhost:8000"
        websocket_client = websocket.WebSocketApp(
            websocket_server_uri,
            on_open=on_open,
            on_message=on_message_handler,
            on_error=on_error_handler,
            on_close=on_close
        )
        websocket_client.run_forever()
    except Exception as e:
        on_error(f"Connection error: {str(e)}")
