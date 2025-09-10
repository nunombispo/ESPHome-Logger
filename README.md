# ESPHome Logger

A Python application for logging sensor data and device states from multiple ESPHome devices to CSV files. This tool continuously monitors ESPHome devices and logs all state changes with timestamps for data analysis and monitoring.

## Features

- **Multi-device support**: Monitor multiple ESPHome devices simultaneously
- **Automatic CSV logging**: Data is automatically saved to CSV files organized by device/room
- **Date-based file organization**: Creates separate CSV files for each day
- **Robust connection handling**: Automatic reconnection with configurable retry intervals
- **Data filtering**: Skips invalid data (NaN values, None states)
- **Environment-based configuration**: Uses `.env` file for secure credential management

## Installation

1. Clone this repository:

```bash
git clone https://github.com/nunombispo/ESPHome-Logger
cd ESPHome-Logger
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your ESPHome device credentials:

```env
# Living Room
API_HOST_LIVINGROOM=192.168.1.100
API_LIVINGROOM_PASSWORD=your_password_here

# Work Room
API_HOST_WORKROOM=192.168.1.101
API_WORKROOM_PASSWORD=your_password_here

# Bedroom
API_HOST_BEDROOM=192.168.1.102
API_BEDROOM_PASSWORD=your_password_here

# Attic
API_HOST_ATTIC=192.168.1.103
API_ATTIC_PASSWORD=your_password_here

# Hallway
API_HOST_HALLWAY=192.168.1.104
API_HALLWAY_PASSWORD=your_password_here
```

## Usage

### Running the Multi-Device Logger

To monitor all configured ESPHome devices:

```bash
python main.py
```

This will start logging data from all devices defined in your `.env` file to separate CSV files in the `logs/` directory.

### Running a Simple Single-Device Logger

For testing with a single device, you can use the simple logger:

```bash
python simple.py
```

Make sure to set `API_HOST` and `API_PASSWORD` in your `.env` file for this to work.

## File Structure

```
ESPHome-Logger/
├── esphome_logger.py    # Main ESPHomeLogger class
├── main.py             # Multi-device logger script
├── simple.py           # Single-device logger script
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── logs/              # CSV log files directory
│   ├── living_room/
│   ├── work_room/
│   ├── bedroom/
│   ├── attic/
│   └── hallway/
└── README.md          # This file
```

## CSV Output Format

The logger creates CSV files with the following columns:

- `timestamp`: ISO format timestamp of the state change
- `entity_id`: Internal ESPHome entity identifier
- `friendly_name`: Human-readable name of the sensor/device
- `state`: Current value of the sensor/device

Example CSV output:

```csv
timestamp,entity_id,friendly_name,state
2025-01-09T10:30:15.123456,1234567890,Temperature Sensor,22.5
2025-01-09T10:30:16.234567,1234567891,Humidity Sensor,45.2
2025-01-09T10:30:17.345678,1234567892,Motion Sensor,true
```

## Configuration

### ESPHomeLogger Class Parameters

- `host`: IP address or hostname of the ESPHome device
- `password`: API password for the ESPHome device (optional)
- `csv_dir`: Directory to store CSV files (default: "logs")
- `retry_interval`: Seconds to wait before retrying connection (default: 15)

### Connection Management

- The logger automatically reconnects if the connection is lost
- Connection timeout is set to 5 minutes - if no data is received for 5 minutes, it assumes disconnection
- Retry interval is configurable per device

## Requirements

- Python 3.7+
- ESPHome devices with API enabled
- Network access to ESPHome devices

## Dependencies

- `aioesphomeapi`: ESPHome API client library
- `python-dotenv`: Environment variable management

## Troubleshooting

### Connection Issues

1. Verify ESPHome devices have API enabled in their configuration
2. Check that the IP addresses in `.env` are correct
3. Ensure passwords are correct
4. Verify network connectivity to ESPHome devices

### Data Issues

1. Check that sensors are properly configured in ESPHome
2. Verify that sensors are sending data (check ESPHome logs)
3. Ensure CSV directories have write permissions

### Log Files

The application provides console output showing:

- Connection status
- State updates with timestamps
- Error messages and retry attempts

## License

This project is open source.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
