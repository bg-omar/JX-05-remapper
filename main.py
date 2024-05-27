import tkinter as tk
from tkinter import ttk
from typing import Self
import bluetooth
from pynput.keyboard import Controller, Key
import asyncio
from bleak import BleakClient, BleakScanner


async def scan_ble_devices():
    print("Scanning for BLE devices...")

    devices = await BleakScanner.discover()

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


# Bluetooth device address of your JX-05 remote ring
device_address = "d8:d2:c7:d2:7b:ad"  # Replace with your device's MAC address BluetoothLE#BluetoothLE00:1a:7d:da:71:13-d8:d2:c7:d2:7b:ad

# Initialize the keyboard controller
keyboard = Controller()


# Function to simulate key press
def press_key(key):
    keyboard.press(key)
    keyboard.release(key)



# Key mappings dictionary
key_mappings = {
    "Button1": Key.media_volume_up,
    "Button2": Key.media_volume_down
}


def update_mapping(button, key):
    key_mappings[button] = key


# Function to handle notifications from the BLE device
def notification_handler(sender, data):
    print(f"Received data: {data}")
    if data == b'Button1':
        press_key(key_mappings["Button1"])
    elif data == b'Button2':
        press_key(key_mappings["Button2"])


async def show_services(client):
    services = await client.get_services()
    for service in services:
        print(f"Service: {service}")
        for char in service.characteristics:
            print(f"  Characteristic: {char}")
            print(f"    Properties: {char.properties}")


async def connect_to_device(address):
    async with BleakClient(address) as client:
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
                    break
            if characteristic_uuid:
                break

        if characteristic_uuid:
            await client.start_notify(characteristic_uuid, notification_handler)
            print(f"Subscribed to notifications for characteristic: {characteristic_uuid}")

            # Keep the connection open to receive notifications
            while True:
                await asyncio.sleep(1)
        else:
            print("No characteristics with notification support found.")


# GUI for key mapping
class KeyMapperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JX-05 Key Mapper")
        self.geometry("300x200")

        self.button1_label = tk.Label(self, text="Button 1")
        self.button1_label.pack(pady=5)
        self.button1_key = ttk.Combobox(self, values=[key for key in dir(Key) if not key.startswith("__")])
        self.button1_key.pack(pady=5)
        self.button1_key.bind("<<ComboboxSelected>>", self.set_button1_key)

        self.button2_label = tk.Label(self, text="Button 2")
        self.button2_label.pack(pady=5)
        self.button2_key = ttk.Combobox(self, values=[key for key in dir(Key) if not key.startswith("__")])
        self.button2_key.pack(pady=5)
        self.button2_key.bind("<<ComboboxSelected>>", self.set_button2_key)

    def set_button1_key(self, event):
        selected_key = self.button1_key.get()
        update_mapping("Button1", getattr(Key, selected_key))

    def set_button2_key(self, event):
        selected_key = self.button2_key.get()
        update_mapping("Button2", getattr(Key, selected_key))


if __name__ == "__main__":
    asyncio.run(scan_ble_devices())
    asyncio.run(connect_to_device(device_address))
    # scan_bluetooth_devices()
    app = KeyMapperApp()
    app.after(100, lambda: asyncio.run(connect_to_device(device_address)))
    app.mainloop()
