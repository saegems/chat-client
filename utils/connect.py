import websocket
import json
import threading
import time


def run_websocket_client(sender, receiver, message, on_success, on_error, on_message):
    """Run a WebSocket client to send a message and handle responses."""

    def on_open(ws):
        try:
            ws.send(json.dumps(
                {"sender": sender, "receiver": receiver, "message": message}))
        except Exception as e:
            on_error(str(e))
            ws.close()

    def on_message_handler(ws, message):
        try:
            data = json.loads(message)
            if data.get("status") != "welcome":
                on_message(data)
            time.sleep(0.1)  # Brief delay
            ws.close()
        except json.JSONDecodeError:
            on_error("Invalid response format")
            ws.close()

    def on_error_handler(ws, error):
        on_error(str(error))

    def on_close(ws, close_status_code, close_msg):
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

        wst = threading.Thread(target=websocket_client.run_forever)
        wst.daemon = True
        wst.start()

    except Exception as e:
        on_error(f"Connection error: {str(e)}")
