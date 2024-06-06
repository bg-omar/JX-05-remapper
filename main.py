import tkinter as tk
from tkinter import ttk
from typing import Self
import bluetooth
import keyboard
from bleak import BleakGATTCharacteristic
from pynput.keyboard import Controller, Key
import asyncio
import bleak

from service_uuid import JX_05, uuids

# HID: 0x1812 # PRIMARY SERVICE
# UUID: 00002A4D-0000-1000-8000-00805F9B34FB
# UUID: 0x2902
# UUID: 0x2908
#
# Read-REPORT_MAP:                            00002A4B-0000-1000-8000-00805F9B34FB
# ReadWriteNotify-BOOT_MOUSE_INPUT_REPORT:    00002A33-0000-1000-8000-00805F9B34FB
# Read-HID_INFORMATION:                       00002A4A-0000-1000-8000-00805F9B34FB
# Write-HID_CONTROL_POINT:                    00002A4C-0000-1000-8000-00805F9B34FB

# Define the UUIDs for the service and characteristic

SERVICE_UUID = uuids["vendor_specific"]
CHAR_UUID = uuids["vendor_specific_write"]
CHAR_UUID_N = uuids["boot_mouse_input_report"]

# Replace MY_CHAR_UUID with the UUID of the characteristic that sends the button press notifications
MY_CHAR_UUID: str =  uuids["vendor_specific_notify"]
service =  uuids["vendor_specific"]
characteristic =  uuids["vendor_specific_notify"]


async def enable_notifications(address, service_uuid, characteristic_uuid):
    async with bleak.BleakClient(address) as client:
        print(f"Forming a connection to {address}")

        client.connect(JX_05)
        print(" - Connected to server")

        # Get services
        services = client.get_services()
        service = services.get_service(service_uuid)
        characteristic = service.get_characteristic(characteristic_uuid)

        print(f" ---> characteristic: {characteristic}")

        # Enable notifications
        await client.start_notify(uuids["report"], notification_handler)

        # Set the client characteristic configuration descriptor
        descriptor_uuid = "00002902-0000-1000-8000-00805f9b34fb"
        descriptor = characteristic.get_descriptor(descriptor_uuid)
        await client.write_gatt_descriptor(descriptor.handle, b"\x01\x00")

        print("Notifications enabled")


async def notification_handler(sender, data):
    print(f"->From sender: {sender}")
    print(f"Received data: {data}")
    pass


async def scan_ble_devices():
    print("Scanning for BLE devices...")

    devices = await bleak.BleakScanner.discover()

    if devices:
        print(f"Found {len(devices)} devices:")
        for device in devices:
            print(f"  {device.address} - {device.name}")
    else:
        print("No devices found")


def scan_bluetooth_devices():
    print("Scanning for Bluetooth devices...")
    devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    if devices:
        print(f"Found {len(devices)} devices:")
        for addr, name in devices:
            print(f"  {addr} - {name}")
    else:
        print("No devices found")


async def show_services(client):
    services = await client.get_services()
    for service in services:
        print(f"Service: {service}")
        for char in service.characteristics:
            print(f"  Characteristic: {char}")
            print(f"    Properties: {char.properties}")


# Bluetooth device address of your JX-05 remote ring
device_address = JX_05  # Replace with your device's MAC address BluetoothLE#BluetoothLE00:1a:7d:da:71:13-d8:d2:c7:d2:7b:ad

# Initialize the keyboard controller
keyboard_controls = Controller()


# Function to handle notifications from the BLE device
def notification_handler(sender, data):
    print(f"->From sender: {sender}")
    print(f"Received data: {data}")


async def connect_to_device(address):
    async with bleak.BleakClient(address) as client:
        print("Connected successfully!")

        # Show all services and characteristics with their properties
        await show_services(client)

        # Subscribe to the first characteristic that supports notifications
        characteristic_uuid = None
        services = await client.get_services()
        for service in services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    characteristic_uuid = char.uuid

            if characteristic_uuid:
                break

        if characteristic_uuid:
            await client.start_notify(characteristic_uuid, notification_handler)
            print(f"Subscribed to notifications for characteristic: {characteristic_uuid}")
            await client.start_notify(uuids["vendor_specific_notify"], callback)
            print(f"Subscribed to notifications for characteristic: {uuids['vendor_specific_notify']}")

            characteristic = service.get_characteristic(characteristic_uuid)
            # Set the client characteristic configuration descriptor
            descriptor_uuid = "00002902-0000-1000-8000-00805f9b34fb"
            descriptor = characteristic.get_descriptor(descriptor_uuid)
            await client.write_gatt_descriptor(descriptor.handle, b"\x01\x00")
            await client.write_gatt_char(uuids["vendor_specific_write"], b"\x01\x00", response=False)
            # Keep the connection open to receive notifications
            while True:
                print(f"Still true")
                try:
                    async with bleak.BleakClient(JX_05) as client:
                        await client.read_gatt_char(uuids["vendor_specific_notify"])
                except bleak.BleakError as e:
                    print(f"Failed to write to characteristic: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                await asyncio.sleep(1)
        else:
            print("No characteristics with notification support found.")





def callback(sender: BleakGATTCharacteristic, data: bytearray):
    print(f"{sender}: {data}")



async def main():
    # Create a client object
    address = JX_05
    print(f"  ---> address:  {address}")
    client = bleak.BleakClient(address)
    print(f"  ---> client:  {client}")

    # Connect to the device
    await client.connect()

    # Subscribe to notifications from the characteristic that sends button press notifications
    await client.start_notify(MY_CHAR_UUID, callback)

    # Wait for notifications to be received
    while True:
        await enable_notifications(JX_05, service, characteristic)
        await asyncio.sleep(1)

    # Stop notifications and disconnect from the device
    await client.stop_notify(MY_CHAR_UUID)
    await client.disconnect()


if __name__ == "__main__":
    # scan_bluetooth_devices()
    # asyncio.run(scan_ble_devices())
    asyncio.run(connect_to_device(device_address))

    #app.after(100, lambda: asyncio.run(connect_to_device(device_address)))


    # asyncio.run(main())
