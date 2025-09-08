import asyncio
from aioesphomeapi import APIClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_HOST = os.getenv("API_HOST")
API_PASSWORD = os.getenv("API_PASSWORD")

async def main():
    # Connect to your ESPHome device by IP or hostname
    client = APIClient(API_HOST, 6053, password=API_PASSWORD, noise_psk=API_PASSWORD)
    await client.connect(login=True)

    # Define a callback function that will be triggered every time
    # the device sends a new state update (sensor reading, switch state, etc.)
    def state_callback(state):
        print("State update:", state)

    # Subscribe to all state updates
    client.subscribe_states(state_callback)

    # Keep the script running so we continue receiving updates
    while True:
        await asyncio.sleep(10)

asyncio.run(main())