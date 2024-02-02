import json

def merge_json_files(meta_path, output_path, merged_path):
    # Load data from meta.json
    with open(meta_path, 'r') as meta_file:
        meta_data = json.load(meta_file)

    # Load data from output.json
    with open(output_path, 'r') as output_file:
        output_data = json.load(output_file)

    # Merge the data
    merged_data = []
    for meta_item, output_item in zip(meta_data, output_data):
        # Extract information from meta.json
        meta_info = meta_item[0]
        num_columns = meta_item[1]
        num_rows = meta_item[2]

        # Extract column data from output.json
        column_data = list(output_item.values())[0]

        # Combine all information
        merged_item = [meta_info] + [num_columns, num_rows, column_data]
        merged_data.append(merged_item)

    # Save the merged data to merged.json
    with open(merged_path, 'w') as merged_file:
        json.dump(merged_data, merged_file, indent=2)

# # Replace 'meta.json', 'output.json', and 'merged.json' with your file paths
# merge_json_files('meta.json', 'output.json', 'merged.json')


# merged_data = json.load(open('merged.json'))
# print(merged_data[0][3])