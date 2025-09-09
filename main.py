import asyncio
from esphome_logger import ESPHomeLogger
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Workroom
API_HOST_WORKROOM=os.getenv("API_HOST_WORKROOM")
API_WORKROOM_PASSWORD=os.getenv("API_WORKROOM_PASSWORD")
# Bedroom
API_HOST_BEDROOM=os.getenv("API_HOST_BEDROOM")
API_BEDROOM_PASSWORD=os.getenv("API_BEDROOM_PASSWORD")
# Living room
API_HOST_LIVINGROOM=os.getenv("API_HOST_LIVINGROOM")
API_LIVINGROOM_PASSWORD=os.getenv("API_LIVINGROOM_PASSWORD")



async def main():
    # Loggers
    devices = [
        {"host": API_HOST_LIVINGROOM, "password": API_LIVINGROOM_PASSWORD, "csv_dir": "logs/living_room"},
        {"host": API_HOST_WORKROOM, "password": API_WORKROOM_PASSWORD, "csv_dir": "logs/work_room"},
        {"host": API_HOST_BEDROOM, "password": API_BEDROOM_PASSWORD, "csv_dir": "logs/bedroom"},
    ]
    # Start loggers
    loggers = [ESPHomeLogger(**dev) for dev in devices]
    await asyncio.gather(*(logger.run() for logger in loggers))

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())