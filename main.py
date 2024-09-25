import uuid
import os
from googleapiclient import discovery
from google.oauth2 import service_account
import json
import base64
from google.cloud import pubsub_v1


project_id = "project-id" # Enter project id
vpc_network = "projects/{project-id}/global/networks/{vpc-name}" # Enter the vpc
subscription_id = "Subscription-to-setup"  # Make sure to set this to your actual Pub/Sub subscription ID

# Path to your service account key file
key_path = ""

def block_ip_from_vpc(source_ip):
    # Use google.oauth2 service account credentials for Python 3
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    service = discovery.build('compute', 'v1', credentials=credentials)

    # Generate a unique identifier for the firewall rule
    unique_id = str(uuid.uuid4())
    rule_name = f"block-ip-{unique_id}"

    firewall_rule = {
        "name": rule_name,
        "network": vpc_network,
        "direction": "INGRESS",
        "priority": 1000,
        "sourceRanges": [source_ip],
        "denied": [
            {
                "IPProtocol": "all"
            }
        ],
    }

    # Insert the firewall rule
    request = service.firewalls().insert(project=project_id, body=firewall_rule)
    response = request.execute()

    print(f"Firewall rule '{rule_name}' created to block IP: {source_ip}")

def process_pubsub_message(message):
    try:
        # Print the entire Pub/Sub message for debugging
        print(f"Received message: {message.data.decode('utf-8')}")

        # Parse the Pub/Sub message
        data = json.loads(message.data.decode("utf-8"))

        # Print the parsed JSON data to understand the structure
        print(f"Parsed data: {json.dumps(data, indent=4)}")

        # Extract the source IP address from the jsonPayload
        source_ip = data.get("jsonPayload", {}).get("source_ip_address")

        if source_ip:
            print(f"Blocking IP: {source_ip}")
            block_ip_from_vpc(source_ip)
        else:
            print("Source IP not found in the message.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

    # Acknowledge the Pub/Sub message
    message.ack()



def listen_for_threats():
    # Initialize the Pub/Sub subscriber client
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Listen to the Pub/Sub subscription
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_pubsub_message)
    print(f"Listening for messages on {subscription_path}...")

    # Keep the main thread alive to keep receiving messages
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    listen_for_threats()
