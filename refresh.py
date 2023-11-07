import requests
import csv

API_URL = "https://api.guildwars2.com/v2/items"
OUTFILE = "items.csv"
FIELDS = ["id", "name", "type", "level", "rarity", "vendor_value"]
BATCH_SIZE = 200

# Get a batch of item detailed information
def get_item_data(item_ids):
    item_ids_str = ','.join(map(str, item_ids))
    url = f"{API_URL}?ids={item_ids_str}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

# Handle the writing and headers
def write_to_csv(data):
    with open(OUTFILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS)
        writer.writeheader()

        for item in data:
            filtered_data = {field: item.get(field, '') for field in FIELDS}
            writer.writerow(filtered_data)

item_ids = []

# Step 1: Retrieve all item IDs
res = requests.get(API_URL)
res.raise_for_status()
item_ids = res.json()

# Step 2: Fetch item data in batches
items = []

for i in range(0, len(item_ids), BATCH_SIZE):
    batch_item_ids = item_ids[i:i + BATCH_SIZE]
    batch_data = get_item_data(batch_item_ids)
    items.extend(batch_data)

# Step 3: Write data to CSV
write_to_csv(items)
