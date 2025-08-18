import websocket


def on_open(websocket):
    print("Callback connection opened.")
    websocket.send("Hello, Server")


def on_message(websocket, message):
    print(f"Received message: {message}")


def on_error(websocket, error):
    print(f"Error: {error}")


def on_close(websocket, close_status_code, close_message):
    print(f"Connection closed with code: {
          close_status_code}, message: {close_message}")


def run_websocket_client():
    websocket_server_uri = "ws://localhost:8000"
    websocket_client = websocket.WebSocketApp(
        websocket_server_uri,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    websocket_client.run_forever()
