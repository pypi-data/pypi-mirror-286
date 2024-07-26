import requests
import json
import uuid
import logging

class PushbulletAPI:
    BASE_URL = "https://api.pushbullet.com/v2"

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Access-Token': self.access_token,
            'Content-Type': 'application/json'
        }
        logging.basicConfig(level=logging.ERROR)

    def _post(self, endpoint, data):
        try:
            response = requests.post(
                f"{self.BASE_URL}/{endpoint}",
                headers=self.headers,
                data=json.dumps(data)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error in _post request to {endpoint}: {e}")
            return {"error": str(e)}

    def _delete(self, endpoint):
        try:
            response = requests.delete(
                f"{self.BASE_URL}/{endpoint}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error in _delete request to {endpoint}: {e}")
            return {"error": str(e)}

    def _generate_guid(self):
        return str(uuid.uuid4())

    def get_current_user(self):
        return self._get("users/me")

    def push_note(self, device_iden, title, body):
        data = {
            "type": "note",
            "title": title,
            "body": body,
            "device_iden": device_iden
        }
        return self._post("pushes", data)

    def push_link(self, device_iden, title, url, body=None):
        data = {
            "type": "link",
            "title": title,
            "url": url,
            "device_iden": device_iden
        }
        if body:
            data["body"] = body
        return self._post("pushes", data)

    def push_file(self, device_iden, file_name, file_type, file_url, body=None):
        data = {
            "type": "file",
            "file_name": file_name,
            "file_type": file_type,
            "file_url": file_url,
            "device_iden": device_iden
        }
        if body:
            data["body"] = body
        return self._post("pushes", data)

    def list_devices(self):
        return self._get("devices")

    def create_text(self, target_device_iden, addresses, message, guid=None, file_url=None, file_type=None, skip_delete_file=True):
        if guid is None:
            guid = self._generate_guid()

        if not addresses or not message or not target_device_iden:
            logging.error("Invalid input: addresses, message, and target_device_iden are required.")
            return {"error": "Invalid input: addresses, message, and target_device_iden are required."}

        data = {
            "data": {
                "addresses": addresses,
                "message": message,
                "target_device_iden": target_device_iden,
                "guid": guid
            },
            "skip_delete_file": skip_delete_file
        }

        if file_url:
            data["file_url"] = file_url
        if file_type:
            data["data"]["file_type"] = file_type

        return self._post("texts", data)

    def update_text(self, iden, addresses, message, guid=None, file_url=None, file_type=None, skip_delete_file=True):
        if guid is None:
            guid = self._generate_guid()

        if not iden or not addresses or not message:
            logging.error("Invalid input: iden, addresses, and message are required.")
            return {"error": "Invalid input: iden, addresses, and message are required."}

        data = {
            "data": {
                "addresses": addresses,
                "message": message,
                "guid": guid
            },
            "skip_delete_file": skip_delete_file,
            "iden": iden
        }

        if file_url:
            data["file_url"] = file_url
        if file_type:
            data["data"]["file_type"] = file_type

        return self._post(f"texts/{iden}", data)

    def delete_text(self, iden):
        if not iden:
            logging.error("Invalid input: iden is required.")
            return {"error": "Invalid input: iden is required."}

        return self._delete(f"texts/{iden}")
