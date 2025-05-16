import requests
import random
import time
from io import BytesIO

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

bearer_token = input("accessToken: ").strip()
username_to_claim = input("username: ").strip()
repeat_count = int(input("threads: ").strip())  # still a loop, not real threads

claim_url = "https://accounts.rec.net/account/me/username"
webhook_url = ""

def create_multipart_formdata(fields):
    boundary = "----WebKitFormBoundarywNvz4YAFgoRF2P6Z"
    lines = []

    for key, value in fields.items():
        lines.append(f"--{boundary}")
        lines.append(f'Content-Disposition: form-data; name="{key}"')
        lines.append('')
        lines.append(value)

    lines.append(f"--{boundary}--")
    lines.append('')

    body = '\r\n'.join(lines)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body.encode(), content_type

def send_webhook_notification(username):
    data = {
        "embeds": [{
            "description": f"ぬ claimed @{username}",
            "color": 65280  # Green color
        }]
    }
    requests.post(webhook_url, json=data)

for attempt in range(repeat_count):
    delay = random.uniform(2, 5)
    print(f"\n[{attempt + 1}/{repeat_count}] attempting to claim '{username_to_claim}' (delay {delay:.2f}s)...")
    time.sleep(delay)

    fields = {
        'username': username_to_claim,
    }

    form_data, content_type = create_multipart_formdata(fields)

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.5",
        "authorization": f"Bearer {bearer_token}",
        "content-type": content_type,
        "origin": "https://rec.net",
        "referer": "https://rec.net/",
        "user-agent": random.choice(USER_AGENTS),
    }

    response = requests.put(
        claim_url,
        headers=headers,
        data=form_data
    )

    print(response.text)

    if response.status_code == 200:
        print(f"Sclaimed '{username_to_claim}'!")
        send_webhook_notification(username_to_claim)
        input("press enter to exit")  # Pauses here
        break
    else:
        print(f"Failed to claim '{username_to_claim}' with status code {response.status_code}")

    time.sleep(random.uniform(2, 5))
