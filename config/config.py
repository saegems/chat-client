from dotenv import load_dotenv
import os

if not load_dotenv():
    raise EnvironmentError(
        "Failed to load .env file. Please ensure it exists and is correctly formatted.")

SERVER = os.getenv("SERVER")
WEBSOCKET_SERVER = os.getenv("WEBSOCKET_SERVER")
FEEDBACK_PAGE_URL = os.getenv("FEEDBACK_PAGE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
INIT_VECTOR = os.getenv("INIT_VECTOR")

if SERVER is None:
    raise ValueError("SERVER environment variable is not set in .env file")
if WEBSOCKET_SERVER is None:
    raise ValueError(
        "WEBSOCKET_SERVER environment variable is not set in .env file")
if FEEDBACK_PAGE_URL is None:
    raise ValueError(
        "FEEDBACK_PAGE_URL environment variable is not set in .env file")
if SECRET_KEY is None:
    raise ValueError(
        "SECRET_KEY environment variable is not set in .env file")
if INIT_VECTOR is None:
    raise ValueError(
        "INIT_VECTOR environment variable is not set in .env file")
