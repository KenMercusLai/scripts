import csv
import re
import sys
import itertools

# Define the input and output file paths
input_file = sys.argv[1]  # Replace with your input file path
output_file = input_file + ".objects.csv"  # Replace with your desired output file path

# Regular expression to match object definitions and their attributes
object_pattern = re.compile(r"^object (\S+)\s+(\S+)\s*$")
attribute_pattern = re.compile(r"^\s+(\S+)\s+(.+)$")


def split_objects(lines: list[str]) -> list[list[str]]:
    objects = []
    current_object = []
    for line in lines:
        object_match = object_pattern.match(line)
        attribute_match = attribute_pattern.match(line)

        if not object_match and not attribute_match:
            if current_object:
                objects.append(current_object)
                current_object = []

        if object_match:
            if current_object:
                objects.append(current_object)
                current_object = []
            current_object.append(line.replace("\n", ""))
        elif current_object and attribute_match:
            current_object.append(line.replace("\n", ""))
    return objects


def parse_object(object: list[str]) -> dict:
    object_def, attribute_def = object[0], object[1:]
    # print(object_def, attribute_def)
    object_type, object_name = object_pattern.match(object_def).groups()
    attributes = []
    # print(attribute_def)
    for i in attribute_def:
        attributes.append(attribute_pattern.match(i).groups())
    return {"name": object_name, "type": object_type, "attributes": attributes}


def get_all_attribute_keys(parsed_object: dict) -> tuple:
    keys = map(lambda x: x[0], parsed_object["attributes"])
    return keys


def write_csv(filename: str, keys: list["str"], data: dict):
    print(filename, keys)
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        for i in data:
            name = i["name"]
            type = i["type"]

            for attr in i["attributes"]:
                attribute_data = []
                # print(attr, attribute_data)
                for j in keys[2:]:
                    if j == attr[0]:
                        attribute_data.append(attr[1])
                    else:
                        attribute_data.append("")
                writer.writerow([name, type, *attribute_data])


if __name__ == "__main__":
    with open(input_file, "r") as file:
        splitted_objects = split_objects(file.readlines())
    print(len(splitted_objects))
    parsed_objects = list(map(parse_object, splitted_objects))
    keys_list = map(get_all_attribute_keys, parsed_objects)
    unique_attribute_keys = set(itertools.chain.from_iterable(keys_list))
    print(unique_attribute_keys)
    write_csv(output_file, ["name", "type"] + list(unique_attribute_keys), parsed_objects)
