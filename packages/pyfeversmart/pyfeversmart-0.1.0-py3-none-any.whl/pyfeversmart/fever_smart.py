"""Fever Smart API"""
import logging

from bluetooth_sensor_state_data import BluetoothData
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorLibrary

DEVICE_SIGNATURE = "0201040303"  # Android app starts with this (so zero index)

FEVER_SMART_MANUFACTURER_ID = 8199

_LOGGER = logging.getLogger(__name__)


class FeverSmartAdvParser(BluetoothData):
    """Date update for Feversmart Bluetooth devices."""

    def __init__(self, key: bytes | None = None) -> None:
        super().__init__()
        self.key = key

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Starting update")
        manufacturer_data = service_info.manufacturer_data

        if not manufacturer_data:
            return

        # Check if we have a feversmart advert
        if FEVER_SMART_MANUFACTURER_ID not in manufacturer_data:
            _LOGGER.debug("Not Feversmart")
            return

        adv_value = manufacturer_data[FEVER_SMART_MANUFACTURER_ID]

        # Convert back to raw bytes
        raw_adv = (
            FEVER_SMART_MANUFACTURER_ID.to_bytes(length=2, byteorder="little")
            + adv_value
        )
        # Only for 0918 message
        # Android app starts with: 0201040303
        hex_adv = "0201040303091817ff" + raw_adv.hex()

        # 0201040303091817ff
        # Flags
        # 02 01 04
        # Servies
        # 03 03 09 18
        # mnf data
        # 17 ff (mnf_id) + message

        message = self.process(hex_adv, self.key)

        _LOGGER.debug("Fever Smart Mac: %s Adv: %s", service_info.address, message)

        device_id = message["device_id"]
        self.set_device_type("Fever Smart", device_id=device_id)
        self.set_device_manufacturer("Nurofen", device_id=device_id)
        self.set_device_name(f"Fever Smart ({device_id})", device_id=device_id)
        self.set_title(f"Fever Smart ({device_id})")

        if "temp" not in message:
            return
        
        self.set_device_sw_version(message["firmware_version"], device_id=device_id)
        self.update_predefined_sensor(
            base_description=SensorLibrary.TEMPERATURE__CELSIUS,
            native_value=message["temp"],
            device_id=device_id)
        self.update_predefined_sensor(
            base_description=SensorLibrary.BATTERY__PERCENTAGE,
            native_value=message["battery"],
            device_id=device_id)

        return

    @staticmethod
    def parse_device_id(hex_device_id: str, flag: bool):
        # if flag:

        # if not flag:
        # Base 16 to 2 then padd to 32
        temp = bin(int(hex_device_id, 16))[2:].zfill(32)

        partA = int(temp[1:6], 2)
        partB = str(int(temp[6:12], 2)).zfill(2)
        partC = int(temp[12:32], 2)

        return chr(partA + 66) + partB + "/" + f"{partC:08}"

    @staticmethod
    def make_key(key, deviceId):
        if len(key) != 8:
            raise Exception("Key wrong length")

        if len(deviceId) != 8:  # first 4 bytes of deviceId
            raise Exception("deviceId wrong length")

        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(key, "utf-8"))
        digest.update(bytes.fromhex(deviceId))
        return digest.finalize()[0:16]

    def decrypt(
        key: str,
        raw_device_id,
        nonce,
        associated_text,  # AEADParameters.associatedText
        encrypted_message,
        mac_size_bytes: int = 4,
    ):
        hashedKey = FeverSmartAdvParser.make_key(key, raw_device_id)
        hashedNonce = bytes.fromhex(nonce)
        hashed_associated_text = bytes.fromhex(associated_text)
        tmp = bytes.fromhex(encrypted_message)

        aesccm = AESCCM(key=hashedKey, tag_length=mac_size_bytes)

        try:
            plaintext = aesccm.decrypt(hashedNonce, tmp, hashed_associated_text)
        except InvalidTag:
            _LOGGER.debug("Could not decrypt message")
            return None

        return plaintext.hex()

    @staticmethod
    def process(raw_offset, key):
        if not raw_offset.startswith(DEVICE_SIGNATURE):
            _LOGGER.debug("Advert does not match starting signature")
            return

        nonce_a = raw_offset[6:16]  # overlaps with patch message
        patch_message_flag = raw_offset[10:14]
        raw_device_id = raw_offset[18:26]
        nonce_b = raw_offset[26:42]
        encrypted_message = raw_offset[42:62]

        # Unknown increasing counter
        some_time = int(raw_offset[26:28], 16)
        device_id = FeverSmartAdvParser.parse_device_id(raw_device_id, False)

        data = {
            "some_time": some_time,
            "device_id": device_id,
            "patch_message_flag": patch_message_flag,
            "raw_message": raw_offset,
        }

        if key is None:
            return data

        message = FeverSmartAdvParser.decrypt(
            key,
            raw_device_id,
            nonce_a + nonce_b,
            raw_offset[10:26],
            encrypted_message,
            4, # Mac size
        )

        if message is None:
            return data

        battery = int(message[4:6], 16)
        raw_temp = int(message[0:4], 16)  # TODO: Deal with int overflow on this...
        firmware_version = str(int(message[6:7], 16)) + "." + str(int(message[7:8], 16))
        counter = int(message[8:12], 16)  # rolling count

        temp = raw_temp * 0.0625

        return {
            "some_time": some_time,
            "device_id": device_id,
            "patch_message_flag": patch_message_flag,
            "raw_message": raw_offset,
            "firmware_version": firmware_version,
            "counter": counter,
            "battery": battery,
            "raw_temp": raw_temp,
            "temp": temp,
        }
