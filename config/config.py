from dotenv import load_dotenv
import os

if not load_dotenv():
    raise EnvironmentError(
        "Failed to load .env file. Please ensure it exists and is correctly formatted.")

SERVER = os.getenv("SERVER")
WEBSOCKET_SERVER = os.getenv("WEBSOCKET_SERVER")

if SERVER is None:
    raise ValueError("SERVER environment variable is not set in .env file")
if WEBSOCKET_SERVER is None:
    raise ValueError(
        "WEBSOCKET_SERVER environment variable is not set in .env file")
