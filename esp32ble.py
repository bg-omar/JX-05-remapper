import asyncio
from bleak import BleakClient, BleakScanner, BleakError

JX_05 = "D8:D2:C7:D2:7B:AD"

# Define the UUIDs for the service and characteristic
uuids = {
    "peripheral_preferred_connection_parameters":   "00002a04-0000-1000-8000-00805f9b34fb",
    "generic_access_profile":                       "00001800-0000-1000-8000-00805f9b34fb",
    "device_name":                                  "00002a00-0000-1000-8000-00805f9b34fb",
    "appearance":                                   "00002a01-0000-1000-8000-00805f9b34fb",

    "generic_attribute_profile":                    "00001801-0000-1000-8000-00805f9b34fb",
    "service_changed":                              "00002a05-0000-1000-8000-00805f9b34fb",

    "device_information":                           "0000180a-0000-1000-8000-00805f9b34fb",
    "manufacturer_name_string":                     "00002a29-0000-1000-8000-00805f9b34fb",
    "model_number_string":                          "00002a24-0000-1000-8000-00805f9b34fb",
    "serial_number_string":                         "00002a25-0000-1000-8000-00805f9b34fb",
    "hardware_revision_string":                     "00002a27-0000-1000-8000-00805f9b34fb",
    "firmware_revision_string":                     "00002a26-0000-1000-8000-00805f9b34fb",
    "software_revision_string":                     "00002a28-0000-1000-8000-00805f9b34fb",
    "system_id":                                    "00002a23-0000-1000-8000-00805f9b34fb",
    "regulatory_cert_data_list":                    "00002a2a-0000-1000-8000-00805f9b34fb",
    "pnp_id":                                       "00002a50-0000-1000-8000-00805f9b34fb",

    "battery_service":                              "0000180f-0000-1000-8000-00805f9b34fb",
    "battery_level":                                "00002a19-0000-1000-8000-00805f9b34fb",

    "hid":                                          "00001812-0000-1000-8000-00805F9B34FB",
    "protocol_mode":                                "00002A4E-0000-1000-8000-00805f9b34fb",
    "report":                                       "00002A4D-0000-1000-8000-00805f9b34fb",
    "report_map":                                   "00002A4B-0000-1000-8000-00805f9b34fb",
    "hid_info":                                     "00002A4A-0000-1000-8000-00805f9b34fb",
    "hid_control":                                  "00002A4C-0000-1000-8000-00805f9b34fb",
    "boot_mouse_input_report":                      "00002A33-0000-1000-8000-00805f9b34fb",

    "vendor_specific":                              "0000ae40-0000-1000-8000-00805f9b34fb",
    "vendor_specific_write":                        "0000ae41-0000-1000-8000-00805f9b34fb",
    "vendor_specific_notify":                       "0000ae42-0000-1000-8000-00805f9b34fb"
}
SERVICE_UUID = uuids["vendor_specific"]
CHAR_UUID = uuids["vendor_specific_notify"]
CHAR_UUID_WRITE = uuids["vendor_specific_write"]

# Global variables to manage connection state
connected = False
device_address = JX_05

async def notification_handler(sender, data):
    print(f"->From sender: {sender}")
    print(f"Received data: {data}")

async def notify_callback(sender, data):
    print(f"Notify callback for characteristic {sender}:")
    print(f"Data length: {len(data)}")
    print(f"Data: {data}")

async def connect_to_server(address, retry_count=3):
    global connected
    for attempt in range(retry_count):
        try:
            async with BleakClient(address) as client:
                print(f"Forming a connection to {address}")

                try:
                    await asyncio.wait_for(client.connect(), timeout=10.0)
                    print(" - Connected to server")
                except asyncio.TimeoutError:
                    print("Connection timed out.")
                    continue
                except BleakError as e:
                    print(f"Failed to connect: {e}")
                    continue

                services = await client.get_services()
                remote_service = services.get_service(SERVICE_UUID)
                if remote_service is None:
                    print(f"Failed to find our service UUID: {SERVICE_UUID}")
                    return False
                print(" - Found our service")

                remote_characteristic = remote_service.get_characteristic(CHAR_UUID)
                if remote_characteristic is None:
                    print(f"Failed to find our characteristic UUID: {CHAR_UUID}")
                    return False
                print(" - Found our characteristic")

                if 'read' in remote_characteristic.properties:
                    value = await client.read_gatt_char(remote_characteristic)
                    print(f"The characteristic value was: {value}")

                if 'notify' in remote_characteristic.properties:
                    await client.start_notify(remote_characteristic, notify_callback)
                    await asyncio.sleep(5)  # Wait for notifications for 5 seconds
                    await client.stop_notify(remote_characteristic)

                connected = True
                return True
        except Exception as e:
            print(f"Exception during connection attempt {attempt + 1}: {e}")
            await asyncio.sleep(1)  # Wait before retrying
    return False

async def write_to_characteristic(address, value, retry_count=3):
    for attempt in range(retry_count):
        try:
            async with BleakClient(address) as client:
                await client.connect()
                await client.write_gatt_char(CHAR_UUID_WRITE, value.encode())
                print(" - Successfully wrote to characteristic")
                return True
        except BleakError as e:
            print(f"Failed to write to characteristic (attempt {attempt + 1}): {e}")
        except Exception as e:
            print(f"Unexpected error during write attempt {attempt + 1}: {e}")
        await asyncio.sleep(1)  # Wait before retrying
    return False

async def main():
    global device_address

    print("Starting BLE scan...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"BLE Advertised Device found: {device}")
        if SERVICE_UUID in [str(s) for s in device.metadata['uuids']]:
            print(f"Found a device advertising the service we are looking for: {device.address}")
            device_address = device.address
            break

    if device_address:
        if await connect_to_server(device_address):
            print("We are now connected to the BLE Server.")
        else:
            print("We have failed to connect to the server; there is nothing more we will do.")
            return
    else:
        print("No suitable device found during the scan.")
        return

    while connected:
        new_value = f"Time since boot: {int(asyncio.get_event_loop().time())}"
        print(f"Setting new characteristic value to \"{new_value}\"")
        if not await write_to_characteristic(device_address, new_value):
            print("Failed to write to characteristic after multiple attempts, exiting.")
            break
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
