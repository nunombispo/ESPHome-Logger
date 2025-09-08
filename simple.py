import asyncio
from aioesphomeapi import APIClient

# Load environment variables
load_dotenv()

async def main():
    # Connect to your ESPHome device by IP or hostname
    client = APIClient(os.getenv("API_HOST"), 6053, password=os.getenv("API_PASSWORD"))
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