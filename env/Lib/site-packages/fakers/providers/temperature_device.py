import requests

BASE_URL = "https://fakers-service.onrender.com"
GET_DEVICE_ENDPOINT = BASE_URL + f"/device/temperature/"
GET_DEVICES_ENDPOINT = BASE_URL + f"/devices/temperature/"
GET_DEVICE_EVENT_PACK_ENDPOINT = BASE_URL + f"/device/temperature/event_pack/"
GET_DEVICES_EVENT_PACK_ENDPOINT = BASE_URL + f"/devices/temperature/event_pack/"


class TemperatureDevice:
    @staticmethod
    def fake_device():
        response = requests.get(GET_DEVICE_ENDPOINT)

        if response.status_code == 200:
            device_info = response.json()
            return device_info
        else:
            print(f"Failed to retrieve temperature device. Status code: {response.status_code}")
            return None

    @staticmethod
    def fake_devices(device_count):
        devices_info = None
        url = GET_DEVICES_ENDPOINT + f"?device_count={device_count}"
        response = requests.get(url)

        if response.status_code == 200:
            devices_info = response.json()
            return devices_info
        else:
            print(f"Failed to retrieve devices. Status code: {response.status_code}")
            return None

    @staticmethod
    def fake_device_event_pack():
        response = requests.get(GET_DEVICE_EVENT_PACK_ENDPOINT)

        if response.status_code == 200:
            device_info = response.json()
            return device_info
        else:
            print(f"Failed to retrieve temperature device's event pack. Status code: {response.status_code}")
            return None

    @staticmethod
    def fake_devices_event_pack(device_count):
        devices_info = None
        url = GET_DEVICES_EVENT_PACK_ENDPOINT + f"?device_count={device_count}"
        response = requests.get(url)

        if response.status_code == 200:
            devices_info = response.json()
            return devices_info
        else:
            print(f"Failed to retrieve devices' event pack. Status code: {response.status_code}")
            return None


# devices = get_temperature_devices(4)
# print(devices[0])
#
# device = get_temperature_device()
# print(device)
#
# devices = get_temperature_devices_event_pack(4)
# print(devices)
#
# device = get_temperature_device_event_pack()
# print(device)

# print(TemperatureDevice.fake_device_event_pack())
