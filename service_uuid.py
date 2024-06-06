JX_05 = "D8:D2:C7:D2:7B:AD"
UnoR4 = "DC:54:75:C3:D9:ED"

# Replace MY_CHAR_UUID with the UUID of the characteristic that sends the button press notifications
MY_CHAR_UUID: str = "00002A33-0000-1000-8000-00805F9B34FB"

# HID: 0x1812 # PRIMARY SERVICE
# UUID: 00002A4D-0000-1000-8000-00805F9B34FB
# UUID: 0x2902
# UUID: 0x2908
#
# Read-REPORT_MAP:                            00002A4B-0000-1000-8000-00805F9B34FB
# ReadWriteNotify-BOOT_MOUSE_INPUT_REPORT:    00002A33-0000-1000-8000-00805F9B34FB
# Read-HID_INFORMATION:                       00002A4A-0000-1000-8000-00805F9B34FB
# Write-HID_CONTROL_POINT:                    00002A4C-0000-1000-8000-00805F9B34FB

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

reads = {
    "peripheral_preferred_connection_parameters": "06 00 09 00 100 00 88 02",
    "generic_access_profile":                     "---",
    "device_name":                                "JX-05",
    "appearance":                                 "193 03",
    "generic_attribute_profile":                  "---",
    "service_changed":                            "Indicate",
    "device_information":                         "---",
    "manufacturer_name_string":                   "zhuhai_jieli",
    "model_number_string":                        "hid_mouse",
    "serial_number_string":                       "48 48 48 48 48 48",
    "hardware_revision_string":                   "0.0.1",
    "firmware_revision_string":                   "0.0.1",
    "software_revision_string":                   "0.0.1",
    "system_id":                                  "00 00 00 00 00 00 00 00",
    "regulatory_cert_data_list":                  "---",
    "pnp_id":                                     "02 AC 05 2C 02 1B 01",
    "battery_service":                            "---",
    "battery_level":                              "88",
    "vendor_specific":                            "---",
    "vendor_specific_write":                      "---",
    "vendor_specific_notify":                     "---"
}

handles = {
  "generic_access_profile": 1,
  "device_name": 2,
  "appearance": 4,
  "peripheral_preferred_connection_parameters": 6,
  "generic_attribute_profile": 8,
  "service_changed": 9,
  "device_information": 12,
  "manufacturer_name_string": 13,
  "model_number_string": 15,
  "serial_number_string": 17,
  "hardware_revision_string": 19,
  "firmware_revision_string": 21,
  "software_revision_string": 23,
  "system_id": 25,
  "regulatory_cert_data_list": 27,
  "pnp_id": 29,
  "battery_service": 31,
  "battery_level": 32,
  "vendor_specific": 74,
  "vendor_specific_write": 75,
  "vendor_specific_notify": 77
}


properties = {
    "device_name": ["read"],
    "appearance": ["read"],
    "peripheral_preferred_connection_parameters": ["read"],
    "service_changed": ["indicate"],
    "manufacturer_name_string": ["read"],
    "model_number_string": ["read"],
    "serial_number_string": ["read"],
    "hardware_revision_string": ["read"],
    "firmware_revision_string": ["read"],
    "software_revision_string": ["read"],
    "system_id": ["read"],
    "regulatory_cert_data_list": ["read"],
    "pnp_id": ["read"],
    "battery_level": ["read", "notify"],
    "vendor_specific_write": ["write-without-response"],
    "vendor_specific_notify": ["notify"]
}


