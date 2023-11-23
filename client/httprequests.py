from client.client import Client
from client.urls import ENDPOINT


def get_lights():
    pass


def get_light_by_id():
    pass


def get_state(light_id: str):
    client = Client()

    state = client.get(f"{ENDPOINT}/{light_id}")

    if not state:
        return []
    return state


def change_state(light_id: str, name: str, value):
    client = Client()
    body = {
        name: value
    }

    return client.put(f"{ENDPOINT}/{light_id}/state", body)
