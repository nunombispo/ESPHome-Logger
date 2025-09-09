import asyncio
import csv
import os
from datetime import datetime, date
from aioesphomeapi import APIClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_HOST = os.getenv("API_HOST")
API_PASSWORD = os.getenv("API_PASSWORD")

# ESPHomeLogger class
class ESPHomeLogger:
    def __init__(self, host, password=None, csv_dir="logs"):
        self.host = host
        self.client = APIClient(host, 6053, password=password, noise_psk=password)
        self.csv_dir = csv_dir
        self.current_date = None
        self.entity_map = {}

        os.makedirs(csv_dir, exist_ok=True)

    # Get the CSV file for the current date
    def _get_csv_file(self):
        today = date.today().isoformat()
        if today != self.current_date:
            self.current_date = today
            self.csv_file = os.path.join(self.csv_dir, f"esphome_{today}.csv")
            if not os.path.exists(self.csv_file):
                with open(self.csv_file, "w", newline="") as f:
                    csv.writer(f).writerow(["timestamp", "entity_id", "friendly_name", "state"])
        return self.csv_file

    # Connect to the ESPHome device
    async def connect(self):
        await self.client.connect(login=True)
        entities, _ = await self.client.list_entities_services()
        self.entity_map = {ent.key: ent.name for ent in entities}
        await self.client.subscribe_states(self._state_callback)

    # State callback
    async def _state_callback(self, state):
        entity_id = state.key
        friendly = self.entity_map.get(entity_id, "unknown")
        value = getattr(state, "state", None)

        with open(self._get_csv_file(), "a", newline="") as f:
            csv.writer(f).writerow([datetime.now().isoformat(), entity_id, friendly, value])

    # Run the logger
    async def run(self):
        print(f"Connecting to {self.host}")
        await self.connect()
        print(f"Connected to {self.host}")
        while True:
            print(f"Sleeping for 10 seconds for {self.host}")
            await asyncio.sleep(10)