import asyncio
from bleak import BleakClient, BleakScanner, BleakError


JX_05 = "D8:D2:C7:D2:7B:AD"

# UUIDs for the services and characteristics
uuids = {
    "hid": "00001812-0000-1000-8000-00805F9B34FB",
    "protocol_mode": "00002A4E-0000-1000-8000-00805f9b34fb",
    "report": "00002A4D-0000-1000-8000-00805f9b34fb",
    "report_map": "00002A4B-0000-1000-8000-00805f9b34fb",
    "hid_info": "00002A4A-0000-1000-8000-00805f9b34fb",
    "hid_control": "00002A4C-0000-1000-8000-00805f9b34fb",
    "boot_mouse_input_report": "00002A33-0000-1000-8000-00805f9b34fb"
}
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


# Global variables to manage connection state
connected = False
device_address = JX_05

async def notification_handler(sender, data):
    print(f"->From sender: {sender}")
    print(f"Received data: {data}")

async def connect_to_server(address, service_uuid, characteristic_uuid, retry_count=3):
    global connected
    for attempt in range(retry_count):
        try:
            async with BleakClient(address) as client:
                print(f"Forming a connection to {address}")

                try:
                    asyncio.wait_for(client.connect(), timeout=30.0)
                    print(" - Connected to server")
                except asyncio.TimeoutError:
                    print("Connection timed out.")
                    continue
                except BleakError as e:
                    print(f"Failed to connect: {e}")
                    continue

                services = await client.get_services()
                service = services.get_service(service_uuid)
                if service is None:
                    print(f"Failed to find service UUID: {service_uuid}")
                    continue
                print(" - Found our service")

                characteristic = service.get_characteristic(characteristic_uuid)
                if characteristic is None:
                    print(f"Failed to find characteristic UUID: {characteristic_uuid}")
                    continue
                print(" - Found our characteristic")

                connected = True
                return client
        except Exception as e:
            print(f"Exception during connection attempt {attempt + 1}: {e}")
            await asyncio.sleep(1)  # Wait before retrying
    return None

async def main():
    print("Starting BLE scan...")
    devices = await BleakScanner.discover()
    device_address = None
    for device in devices:
        print(f"BLE Advertised Device found: {device}")
        if JX_05 == device.address:
            print(f"Found the device we are looking for: {device.address}")
            device_address = device.address
            break

    if device_address:
        client = await connect_to_server(device_address, SERVICE_UUID, CHAR_UUID)
        if client:
            print("We are now connected to the BLE Server.")
            await client.disconnect()
        else:
            print("We have failed to connect to the server; there is nothing more we will do.")
    else:
        print("Device not found during the scan.")

if __name__ == "__main__":
    asyncio.run(main())
