import asyncio
import csv
import os
from datetime import datetime, date
from aioesphomeapi import APIClient
from aioesphomeapi.core import APIConnectionError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_HOST = os.getenv("API_HOST")
API_PASSWORD = os.getenv("API_PASSWORD")

# ESPHomeLogger class
class ESPHomeLogger:
    def __init__(self, host, password=None, csv_dir="logs", retry_interval=15):
        self.host = host
        self.client = APIClient(host, 6053, password=password, noise_psk=password)
        self.csv_dir = csv_dir
        self.current_date = None
        self.entity_map = {}
        self.retry_interval = retry_interval
        self.connected = False

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
        try:
            await self.client.connect(login=True)
            entities, _ = await self.client.list_entities_services()
            self.entity_map = {ent.key: ent.name for ent in entities}
            self.client.subscribe_states(self._state_callback)
            self.connected = True
            print(f"Successfully connected to {self.host}")
        except APIConnectionError as e:
            self.connected = False
            print(f"Connection failed to {self.host}: {e}")
            raise
        except Exception as e:
            self.connected = False
            print(f"Unexpected error connecting to {self.host}: {e}")
            raise

    # State callback
    def _state_callback(self, state):
        entity_id = state.key
        friendly = self.entity_map.get(entity_id, "unknown")
        value = getattr(state, "state", None)

        if value is None or value == "nan":
            return

        with open(self._get_csv_file(), "a", newline="") as f:
            csv.writer(f).writerow([datetime.now().isoformat(), entity_id, friendly, value])
            print(f"State update: {self.host} - {entity_id} - {friendly} - {value}")

    # Run the logger with retry logic
    async def run(self):
        while True:
            try:
                if not self.connected:
                    print(f"Connecting to {self.host}")
                    await self.connect()
                
                # Keep the connection alive
                await asyncio.sleep(10)
                print(f"Sleeping for 10 seconds for {self.host}")

            except APIConnectionError as e:
                print(f"Connection lost to {self.host}: {e}")
                self.connected = False
                print(f"Retrying connection to {self.host} in {self.retry_interval} seconds...")
                await asyncio.sleep(self.retry_interval)
                
            except Exception as e:
                print(f"Unexpected error with {self.host}: {e}")
                self.connected = False
                print(f"Retrying connection to {self.host} in {self.retry_interval} seconds...")
                await asyncio.sleep(self.retry_interval)