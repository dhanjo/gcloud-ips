# Overview

This script automates the blocking of malicious IP addresses in your GCP VPC network. It listens to a Pub/Sub subscription for security notifications (such as those from the Security Command Center or Cloud Logging), extracts the source IP addresses from these messages, and creates firewall rules to block traffic from these IPs.

# Prerequisites

* **Google Cloud Project**: An active GCP project where you have the necessary permissions.
* **Python 3.x**: Ensure Python 3 is installed on your system.
* **Google Cloud SDK** (optional but recommended): For managing GCP resources via the command line.
* **APIs Enabled**:
  - Compute Engine API
  - Pub/Sub API
* **Service Account**: With the following roles:
  - Compute Security Admin (for managing firewall rules)
  - Pub/Sub Subscriber (for reading messages from the subscription)
* **Pub/Sub Subscription**: Set up to receive security notifications.
* **VPC Network**: The network where firewall rules will be applied.

# Setup and Installation:

`pip install google-api-python-client google-auth google-cloud-pubsub`

## Configuration Example

Configure the following variables in the script:

```python
project_id = "project-id"  # Enter project id
vpc_network = "projects/{project-id}/global/networks/{vpc-name}"  # Enter the VPC
subscription_id = "Subscription-to-setup"  # Make sure to set this to your actual Pub/Sub subscription ID
key_path = ""  # Path to your service account key file
```
