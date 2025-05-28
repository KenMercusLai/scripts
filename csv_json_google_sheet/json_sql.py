import json
import sys


# Function to convert JSON to SQL INSERT statements
def json_to_sql(json_data, table_name, output_file):
    with open(output_file, "w") as sql_file:
        for item in json_data:
            # Extract 'match' and 'update' fields
            match = item.get("match", {})
            update = item.get("update", {})
            resource = item.get("resource", "")

            # Construct the JSON object to be inserted
            json_object = {"resource": resource, "match": match, "update": update}

            # Create the SQL INSERT statement
            sql_statement = f"INSERT INTO {table_name} (job_detail) VALUES ('{json.dumps(json_object)}'::jsonb) ON CONFLICT DO NOTHING;\n"
            sql_file.write(sql_statement)


# Main function
def main():
    input_file = sys.argv[1]  # Path to your input JSON file
    output_file = sys.argv[1] + ".sql"  # Path to the output SQL file
    table_name = "q_netbox"  # Name of your target table

    # Read the JSON data from the input file
    with open(input_file, "r") as file:
        json_data = json.load(file)

    # Convert JSON data to SQL INSERT statements
    json_to_sql(json_data, table_name, output_file)
    print(f"SQL INSERT statements have been written to {output_file}")


if __name__ == "__main__":
    main()
