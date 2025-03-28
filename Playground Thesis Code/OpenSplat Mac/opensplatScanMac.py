import asyncio
from bleak import BleakScanner, BleakClient

TARGET_NAME = ["SPLAT", "Splat"]  # Names to look for

async def scan_and_connect():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    for device in devices:
        if device.name in TARGET_NAME:
            print(f"Found {device.name} at {device.address}")

            try:
                async with BleakClient(device.address) as client:
                    print("Connected!")
            except Exception as e:
                print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(scan_and_connect())
