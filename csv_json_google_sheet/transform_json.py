import json
import sys

# Step 1: Read the JSON file
with open(sys.argv[1], "r") as file:
    data = json.load(file)

# Step 2: Transform the data
transformed_data = [
    {
        "resource": "dcim/sites",
        "match": {
            "cf_siteid": item["cf_siteid"],
        },
        "update": {"custom_fields.site_360_photo_date": item["custom_fields.site_360_photo_date"]},
    }
    for item in data
]

# Step 3: Save the transformed data to a new JSON file
with open(f"transformed_{sys.argv[1]}.json", "w") as file:
    json.dump(transformed_data, file, indent=4)

print("Data transformation complete. Transformed data saved to 'transformed_data.json'.")
