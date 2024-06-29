import json

# Step 1: Load the original JSON data
with open('ai_wikipedia_summaries_checkpoint.json', 'r') as file:
    data = json.load(file)

# Step 2: Modify the JSON data
modified_data = {key: {'data': value, 'ai_generated': 1} for key, value in data.items()}
with open('wikipedia/human_wikipedia_summaries.json', 'r') as file:
    data = json.load(file)
    for key, value in data.items():
        modified_data[key] = {'data': value, 'ai_generated': 0}
# Step 3: Write the modified JSON to a new file
with open('modified_file.json', 'w') as file:
    json.dump(modified_data, file, indent=4)