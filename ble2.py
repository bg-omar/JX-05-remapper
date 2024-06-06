import tkinter as tk
import asyncio
from bleak import BleakClient, BleakError
from pynput.keyboard import Controller
import threading

from service_uuid import uuids

# Bluetooth device address and characteristic UUID
JX_05 = "D8:D2:C7:D2:7B:AD"
MY_CHAR_UUID = uuids["vendor_specific_notify"]

# Initialize the keyboard controller
keyboard_controls = Controller()

# Key mappings dictionary
key_mappings = {
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5'
}


service = uuids["vendor_specific"]
characteristic =  uuids["vendor_specific_notify"]


async def enable_notifications(address, service_uuid, characteristic_uuid):
    async with BleakClient(address) as client:
        # Get the characteristic
        characteristic = await client.get_characteristic(service_uuid)
        print(f" ---> characteristic: {characteristic}")


        # Enable notifications
        await client.start_notify(characteristic.handle, notification_handler)

        # Set the client characteristic configuration descriptor
        descriptor_uuid = "00002902-0000-1000-8000-00805f9b34fb"
        descriptor = await client.get_descriptor(characteristic.handle, descriptor_uuid)
        await client.write_gatt_descriptor(descriptor.handle, b"\x01\x00")


async def show_services(client):
    services = await client.get_services()
    for service in services:
        print(f"Service: {service}")
        for char in service.characteristics:
            print(f"  Characteristic: {char}")
            print(f"    Properties: {char.properties}")


def notification_handler(sender, data):
    print(f"Notification from {sender}: {data}")
    # Debugging: print the raw data received
    print(f"Raw notification data: {data}")

    if sender == MY_CHAR_UUID:
        # Assuming the first byte of data indicates the button pressed
        button_pressed = data[0]
        print(f"Button pressed: {button_pressed}")

        if button_pressed in key_mappings:
            press_key(key_mappings[button_pressed])


def press_key(key):
    print(f"Pressing key: {key}")  # Debugging: print the key being pressed
    keyboard_controls.press(key)
    keyboard_controls.release(key)


async def connect_to_device(address):
    try:
        async with BleakClient(address) as client:
            print("Connected successfully!")
            await show_services(client)
            await client.start_notify(MY_CHAR_UUID, notification_handler)
            print(f"Subscribed to notifications for characteristic: {MY_CHAR_UUID}")

            await enable_notifications(JX_05, service, characteristic)
            while True:
                new_value = f"Time since boot: {int(asyncio.get_event_loop().time())}"
                print(f"new char value to \"{new_value}\"")
                try:
                    async with BleakClient(JX_05) as client:
                        await client.write_gatt_char(MY_CHAR_UUID, new_value.encode())
                        print(" - Successfully wrote to characteristic")
                except BleakError as e:
                    print(f"Failed to write to characteristic: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                await asyncio.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")


def start_ble_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(connect_to_device(JX_05))


class KeyMapperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JX-05 Key Mapper")
        self.geometry("300x200")

        self.info_label = tk.Label(self, text="Press buttons on your JX-05 device to send key events 1-5.")
        self.info_label.pack(pady=20)


if __name__ == "__main__":
    app = KeyMapperApp()

    ble_thread = threading.Thread(target=start_ble_loop)
    ble_thread.daemon = True
    ble_thread.start()

    app.mainloop()
