from zeep import Client
from zeep.transports import Transport
from requests import Session
import json
import time

# --- Setup with API Key Header ---
session = Session()
transport = Transport(session=session)

# --- Connect to WSDL ---
client = Client("http://localhost:8002/?wsdl", transport=transport)

# --- Test Calls ---
# Create items
# ------------------
print("Adding an item...")
item1 = client.service.create_item(8,"teste8","teste8")
time.sleep(5)
time.sleep(5)
print("DONE")
# Get all Items -----------
print("Printing List of Items...")
teste=(client.service.get_items())
print(str(teste))
print("DONE")
time.sleep(5)
# Get Specific Item
print("Getting the book with the id 8 ...")
print(client.service.get_item(8))
