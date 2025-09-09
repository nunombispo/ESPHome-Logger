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
# Attic
API_HOST_ATTIC=os.getenv("API_HOST_ATTIC")
API_ATTIC_PASSWORD=os.getenv("API_ATTIC_PASSWORD")
# Hallway
API_HOST_HALLWAY=os.getenv("API_HOST_HALLWAY")
API_HALLWAY_PASSWORD=os.getenv("API_HALLWAY_PASSWORD")


async def main():
    devices = [
        {"host": API_HOST_LIVINGROOM, "password": API_LIVINGROOM_PASSWORD, "csv_dir": "logs/living_room"},
        {"host": API_HOST_WORKROOM, "password": API_WORKROOM_PASSWORD, "csv_dir": "logs/work_room"},
        {"host": API_HOST_BEDROOM, "password": API_BEDROOM_PASSWORD, "csv_dir": "logs/bedroom"},
        {"host": API_HOST_ATTIC, "password": API_ATTIC_PASSWORD, "csv_dir": "logs/attic"},
        {"host": API_HOST_HALLWAY, "password": API_HALLWAY_PASSWORD, "csv_dir": "logs/hallway"},
    ]
    loggers = [ESPHomeLogger(**dev) for dev in devices]
    await asyncio.gather(*(logger.run() for logger in loggers))

if __name__ == "__main__":
    asyncio.run(main())