from splunk_data_sender import SplunkSender
import random
import requests
import time
import json
from datetime import datetime, timedelta

splunk_conf = {
    'endpoint': 'localhost',
    'protocol': 'http',
    'port': '8990',
    'token': 'b2596ab6-c67d-467c-a26d-0dc6c45ab488',
    'index': 'main',
    'verify': False,
    'max_buf_size': 1000,
}

splunk = SplunkSender(**splunk_conf)


def generate_event(num_events=3000):
    event_types = ['INFO', 'ERROR', 'DEBUG', 'WARN']
    user_ids = [f'user_{i}' for i in range(1, 101)]
    messages = [
        'User login successful',
        'User login failed',
        'File uploaded',
        'File download initiated',
        'System error encountered',
        'Configuration updated',
        'User logged out',
        'Permission denied',
        'Resource not found',
        'Operation completed successfully'
    ]

    events = []
    for _ in range(num_events):
        event = {
            'timestamp': (datetime.now() - timedelta(seconds=random.randint(0, 3600))).isoformat(),
            'event_type': random.choice(event_types),
            'user_id': random.choice(user_ids),
            'message': random.choice(messages)
        }
        events.append(event)

    return events


def send_to_splunk(events, splunk_server, hec_token):
    url = f"http://{splunk_server}:8000/services/collector/event"
    headers = {
        "Authorization": f"Splunk {hec_token}",
        "Content-Type": "application/json"
    }

    for event in events:
        data = {
            "event": event
        }
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        if response.status_code != 200:
            print(f"Error sending event: {response.text}")


# Example usage
if __name__ == "__main__":
    for event in generate_event():
        splunk.send_data(event)

    # We finished processing our stuff, we must commit any remaining events to Splunk
    splunk.flush_buffer()
