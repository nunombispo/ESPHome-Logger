import asyncio
from aioesphomeapi import APIClient

async def main():
    # Connect to your ESPHome device by IP or hostname
    client = APIClient("192.168.1.50", 6053, password="your_api_pass")
    await client.connect(login=True)

    # Define a callback function that will be triggered every time
    # the device sends a new state update (sensor reading, switch state, etc.)
    async def state_callback(state):
        print("State update:", state)

    # Subscribe to all state updates
    await client.subscribe_states(state_callback)

    # Keep the script running so we continue receiving updates
    while True:
        await asyncio.sleep(10)

asyncio.run(main())